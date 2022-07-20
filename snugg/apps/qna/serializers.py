from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiTypes, extend_schema_field
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from snugg.apps.user.serializers import UserPublicSerializer

from .models import Answer, Comment, Field, Post


class FieldField(serializers.RelatedField):
    queryset = Field.objects.all()

    def to_internal_value(self, data):
        queryset = self.get_queryset()

        try:
            field = queryset.get(name__iexact=data)
        except Field.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 분야(field)입니다.")

        return field

    def to_representation(self, value):
        return value.name


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    field = FieldField()
    writer = UserPublicSerializer(read_only=True)
    tags = TagListSerializerField(required=False)

    class Meta:
        model = Post
        fields = (
            "pk",
            "field",
            "writer",
            "title",
            "content",
            "created_at",
            "updated_at",
            "accepted_answer",
            "tags",
        )
        read_only_fields = ("created_at", "updated_at")

    def validate_accepted_answer(self, value):
        if value is not None:
            if self.instance is None:
                raise serializers.ValidationError("질문이 만들어지기 전에 답변을 채택할 수 없습니다.")

            if value.post != self.instance:
                raise serializers.ValidationError("이 질문에 달린 답변만 채택할 수 있습니다.")

            if value.writer == self.context.get("request").user:
                raise serializers.ValidationError("자신의 답변은 채택할 수 없습니다.")

        return value

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["writer"] = user

        return super().create(validated_data)


class AnswerSerializer(serializers.ModelSerializer):
    writer = UserPublicSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Answer
        fields = (
            "pk",
            "post",
            "writer",
            "content",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("writer", "created_at", "updated_at")

    def validate_post(self, post):
        if post.accepted_answer is not None:
            raise serializers.ValidationError("이미 답변이 채택된 질문입니다.")

        user = self.context.get("request").user

        if post.answer_set.filter(writer=user).exists():
            raise serializers.ValidationError("이미 답변을 단 질문입니다.")

        return post

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["writer"] = user

        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    writer = UserPublicSerializer(read_only=True)
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "pk",
            "content_type",
            "object_id",
            "writer",
            "content",
            "replies_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "created_at",
            "updated_at",
            "writer",
        )
        extra_kwargs = {
            "object_id": {"write_only": True, "required": False},
            "content_type": {"write_only": True, "required": False},
        }

    def validate(self, data):
        object_id = data.get("object_id", None)
        content_type = data.get("content_type", None)

        if content_type == ContentType.objects.get_for_model(Comment).id:
            parent = Comment.objects.filter(
                content_type=content_type,
                object_id=object_id,
            )
            if parent.content_type == ContentType.objects.get_for_model(Comment).id:
                raise serializers.ValidationError("대댓글까지만 가능합니다.")

        return data

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["writer"] = user

        return super().create(validated_data)

    @extend_schema_field(OpenApiTypes.INT)
    def get_replies_count(self, comment):
        return Comment.objects.filter(
            content_type__comment__object_id=comment.id
        ).count()


class CommentPostSerializer(CommentSerializer):
    target = Post


class CommentAnswerSerializer(CommentSerializer):
    target = Answer


class ReplySerializer(CommentSerializer):
    target = Comment
    writer = UserPublicSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "pk",
            "content_type",
            "object_id",
            "writer",
            "content",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at", "writer")
        extra_kwargs = {
            "object_id": {"required": False, "write_only": True},
            "content_type": {"required": False, "write_only": True},
        }
