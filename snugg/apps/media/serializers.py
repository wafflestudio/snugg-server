from uuid import uuid4

from django.utils.text import slugify
from rest_framework import serializers

from snugg.apps.user.serializers import UserSerializer

from .models import Directory


class DirectorySerializer(serializers.ModelSerializer):
    uploader = UserSerializer(read_only=True)

    class Meta:
        model = Directory
        fields = (
            "pk",
            "uploader",
            "path",
            "filenames",
            "created_at",
        )
        read_only_fields = ("path", "created_at")

    def validate_filenames(self, value):
        # Slugify the filenames.
        return [slugify(filename, allow_unicode=True) for filename in value]

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data["uploader"] = user
        validated_data["path"] = "/".join(["media", str(user.pk), str(uuid4()), ""])

        return super().create(validated_data)
