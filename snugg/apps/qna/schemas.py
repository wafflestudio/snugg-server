from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from .serializers import PostSerializer

post_viewset_schema = extend_schema_view(
    create=extend_schema(
        summary="Create QNA Post",
        description="Create new post on the QNA board.",
        responses={
            201: OpenApiResponse(response=PostSerializer),
            400: OpenApiResponse(description="Invalid or insufficient data."),
            401: OpenApiResponse(
                description="Missing authentication header, or access token expired."
            ),
        },
    ),
    retrieve=extend_schema(
        summary="Retrieve QNA Post",
        description="Retrieve a post on the QNA board.",
        responses={
            200: OpenApiResponse(response=PostSerializer),
            404: OpenApiResponse(description="Post for given id not found"),
        },
    ),
    list=extend_schema(
        summary="List QNA Post",
        description="List the posts on the QNA board.",
        parameters=[
            OpenApiParameter(name="search", description="Search Parameters"),
            OpenApiParameter(
                name="search_type",
                description="Customize search type with comma-seperate fields",
            ),
        ],
    ),
    update=extend_schema(
        summary="Update QNA Post",
        description="Update a post on the QNA board.",
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
        summary="Partial Update QNA Post",
        description="Partially update a post on the QNA board.",
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
        summary="Destroy QNA Post",
        description="Destroy a post on the QNA board.",
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
