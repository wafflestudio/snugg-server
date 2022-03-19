from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from .models import Post


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

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
        read_only_fields = ("writer", "created_at", "updated_at")
        extra_kwargs = {"field": {"required": True}}

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
