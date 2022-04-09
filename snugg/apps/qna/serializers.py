from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from snugg.apps.user.serializers import UserSerializer

from .models import Answer, Field, Post


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
    writer = UserSerializer(read_only=True)
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

        return value

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["writer"] = user

        return super().create(validated_data)


class AnswerSerializer(serializers.ModelSerializer):
    writer = UserSerializer()

    class Meta:
        model = Answer
        fields = (
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

        return post

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["writer"] = user

        return super().create(validated_data)
