from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view

from .serializers import DirectorySerializer

presigned_viewset_schema = extend_schema_view(
    create=extend_schema(
        summary="Batch Presigned Post",
        description="### Do not use 'multipart/form' or 'application/x-www-form-urlencoded'",
        responses={
            201: OpenApiResponse(response=DirectorySerializer),
            400: OpenApiResponse(description="Invalid or insufficient data."),
            401: OpenApiResponse(
                description="Missing authentication header, or access token expired."
            ),
        },
    ),
)
