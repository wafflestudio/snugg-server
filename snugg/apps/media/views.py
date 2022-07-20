from rest_framework.viewsets import GenericViewSet, mixins

from snugg.s3 import create_presigned_post

from .models import Directory
from .serializers import DirectorySerializer


class PresignedURLViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = DirectorySerializer
    queryset = Directory.objects

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        path = response.data["path"]
        filenames = response.data["filenames"]

        presigned_posts = []
        for filename in filenames:
            presigned_posts.append(
                create_presigned_post(
                    path + filename,
                    conditions=[
                        ["content-length-range", 0, 10485760],
                    ],
                )
            )
        response.data["presigned_posts"] = presigned_posts

        return response
