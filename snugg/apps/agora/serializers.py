from rest_framework import serializers

from .models import Lecture


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
