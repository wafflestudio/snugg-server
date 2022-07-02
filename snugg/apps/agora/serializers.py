from rest_framework import serializers

from snugg.apps.user.serializers import UserSerializer

from .models import Lecture, Post


class LectureSerializer(serializers.ModelSerializer):
    university = serializers.SlugRelatedField(slug_field="name", read_only=True)
    college = serializers.SlugRelatedField(slug_field="name", read_only=True)
    major = serializers.SlugRelatedField(slug_field="name", read_only=True)
    semesters = serializers.StringRelatedField(many=True)

    class Meta:
        model = Lecture
        fields = (
            "pk",
            "name",
            "lecture_id",
            "instructor",
            "university",
            "college",
            "major",
            "semesters",
        )


class LectureField(serializers.RelatedField):
    queryset = Lecture.objects.all()

    def to_internal_value(self, data):
        queryset = self.get_queryset()

        try:
            lecture = queryset.get(pk=data)
        except Lecture.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 강의입니다.")

        return lecture

    def to_representation(self, value):
        return LectureSerializer(value).data


class PostSerializer(serializers.ModelSerializer):
    lecture = LectureField()
    writer = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            "pk",
            "lecture",
            "writer",
            "title",
            "content",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["writer"] = user

        return super().create(validated_data)
