from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view

from .serializers import LectureSerializer, StorySerializer

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

story_viewset_schema = extend_schema_view(
    create=extend_schema(
        summary="Create Agora Story",
        description="Create new story on Agora.",
        responses={
            201: OpenApiResponse(response=StorySerializer),
            400: OpenApiResponse(description="Invalid or insufficient data."),
            401: OpenApiResponse(
                description="Missing authentication header, or access token expired."
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve Agora Story",
        description="Retrieve a story from Agora.",
        responses={
            200: OpenApiResponse(response=StorySerializer),
            404: OpenApiResponse(description="Story for given id not found."),
        },
    ),
    list=extend_schema(
        summary="List Agora Storys",
        description="List storys on Agora board.",
    ),
    update=extend_schema(
        summary="Update Agora Story",
        description="Update a story on Agora board.",
        responses={
            200: OpenApiResponse(response=StorySerializer),
            400: OpenApiResponse(description="Invalid or insufficient data."),
            401: OpenApiResponse(
                description="Missing authentication header, or access token expired."
            ),
            403: OpenApiResponse(
                description="Requesting user is not the owner of the story."
            ),
            404: OpenApiResponse(description="Story for given id not found."),
        },
    ),
    partial_update=extend_schema(
        summary="Partial Update Agora Story",
        description="Partially update a story on Agora board.",
        responses={
            200: OpenApiResponse(response=StorySerializer),
            400: OpenApiResponse(description="Invalid data."),
            401: OpenApiResponse(
                description="Missing authentication header, or access token expired."
            ),
            403: OpenApiResponse(
                description="Requesting user is not the owner of the story."
            ),
            404: OpenApiResponse(description="Story for given id not found."),
        },
    ),
    destroy=extend_schema(
        summary="Destroy Agora Story",
        description="Destroy a story on Agora board.",
        responses={
            204: OpenApiResponse(description="No response body."),
            401: OpenApiResponse(
                description="Missing authentication header, or access token expired."
            ),
            403: OpenApiResponse(
                description="Requesting user is not the owner of the story."
            ),
            404: OpenApiResponse(description="Story for given id not found."),
        },
    ),
)
