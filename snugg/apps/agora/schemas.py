from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view

from .serializers import LectureSerializer, PostSerializer

lecture_viewset_schema = extend_schema_view(
    retrieve=extend_schema(
        summary="Retreive Agora Lecture",
        description="Retrieve a lecture from Agora.",
        responses={
            200: OpenApiResponse(response=LectureSerializer),
            404: OpenApiResponse(description="Lecture for given id not found."),
        },
    ),
    list=extend_schema(
        summary="List Agora Lectures", description="List lectures on Agora."
    ),
)

post_viewset_schema = extend_schema_view(
    create=extend_schema(
        summary="Create Agora Post",
        description="Create new post on Agora.",
        responses={
            201: OpenApiResponse(response=PostSerializer),
            400: OpenApiResponse(description="Invalid or insufficient data."),
            401: OpenApiResponse(
                description="Missing authentication header, or access token expired."
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Agora Post",
        description="Retrieve a post from Agora.",
        responses={
            200: OpenApiResponse(response=PostSerializer),
            404: OpenApiResponse(description="Post for given id not found."),
        },
    ),
    list=extend_schema(
        summary="List Agora Posts",
        description="List posts on Agora board.",
    ),
    update=extend_schema(
        summary="Update Agora Post",
        description="Update a post on Agora board.",
        responses={
            200: OpenApiResponse(response=PostSerializer),
            400: OpenApiResponse(description="Invalid or insufficient data."),
            401: OpenApiResponse(
                description="Missing authentication header, or access token expired."
            ),
            403: OpenApiResponse(
                description="Requesting user is not the owner of the post."
            ),
            404: OpenApiResponse(description="Post for given id not found."),
        },
    ),
    partial_update=extend_schema(
        summary="Partial Update Agora Post",
        description="Partially update a post on Agora board.",
        responses={
            200: OpenApiResponse(response=PostSerializer),
            400: OpenApiResponse(description="Invalid data."),
            401: OpenApiResponse(
                description="Missing authentication header, or access token expired."
            ),
            403: OpenApiResponse(
                description="Requesting user is not the owner of the post."
            ),
            404: OpenApiResponse(description="Post for given id not found."),
        },
    ),
    destroy=extend_schema(
        summary="Destroy Agora Post",
        description="Destroy a post on Agora board.",
        responses={
            204: OpenApiResponse(description="No response body."),
            401: OpenApiResponse(
                description="Missing authentication header, or access token expired."
            ),
            403: OpenApiResponse(
                description="Requesting user is not the owner of the post."
            ),
            404: OpenApiResponse(description="Post for given id not found."),
        },
    ),
)
