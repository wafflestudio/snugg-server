from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)

from .serializers import (
    CommentAnswerSerializer,
    CommentPostSerializer,
    CommentSerializer,
    PostSerializer,
    ReplySerializer,
)

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

comment_create_view = extend_schema(
    summary="Create Comment with parent's id",
    description="Create the Comments. ?answer={answer_id} or ?post={post_id} or ?comment={comment_id}",
    parameters=[
        OpenApiParameter(
            name="answer",
            description="Answer id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(name="post", description="Post id", type=OpenApiTypes.INT),
        OpenApiParameter(
            name="comment", description="Comment id", type=OpenApiTypes.INT
        ),
    ],
    responses={
        201: OpenApiResponse(response=CommentAnswerSerializer),
        400: OpenApiResponse(description="Invalid or insufficient data."),
        401: OpenApiResponse(
            description="Missing authentication header, or access token expired."
        ),
        404: OpenApiResponse(description="Parent not found."),
    },
)

comment_list_view = extend_schema(
    summary="List Comments with parent's id",
    description="List the Comments. ?answer={answer_id} or ?post={post_id} or ?comment={comment_id}",
    parameters=[
        OpenApiParameter(name="answer", description="Answer id", type=OpenApiTypes.INT),
        OpenApiParameter(name="post", description="Post id", type=OpenApiTypes.INT),
        OpenApiParameter(
            name="comment", description="Comment id", type=OpenApiTypes.INT
        ),
    ],
    responses={
        200: OpenApiResponse(response=CommentSerializer),
        400: OpenApiResponse(description="Invalid or insufficient data."),
        404: OpenApiResponse(description="Parent not found."),
    },
)

comment_viewset_schema = extend_schema_view(
    retrieve=extend_schema(
        summary="Retrieve Comment",
        description="Retrieve a comment",
        responses={
            200: OpenApiResponse(response=CommentSerializer),
            404: OpenApiResponse(description="Comment for given id not found"),
        },
    ),
    update=extend_schema(
        summary="Update Comment",
        description="Update a comment.",
        responses={
            200: OpenApiResponse(response=CommentSerializer),
            400: OpenApiResponse(description="Invalid or insufficient data."),
            401: OpenApiResponse(
                description="Missing authentication header, or access token expired."
            ),
            403: OpenApiResponse(
                description="Requesting user is not the owner of the comment."
            ),
            404: OpenApiResponse(description="Comment for given id not found."),
        },
    ),
    partial_update=extend_schema(
        summary="Partial Update Comment",
        description="Partially update a comment.",
        responses={
            200: OpenApiResponse(response=CommentSerializer),
            400: OpenApiResponse(description="Invalid data."),
            401: OpenApiResponse(
                description="Missing authentication header, or access token expired."
            ),
            403: OpenApiResponse(
                description="Requesting user is not the owner of the comment."
            ),
            404: OpenApiResponse(description="Comment for given id not found."),
        },
    ),
    destroy=extend_schema(
        summary="Destroy Comment",
        description="Destroy a Comment",
        responses={
            204: OpenApiResponse(description="No response body."),
            401: OpenApiResponse(
                description="Missing authentication header, or access token expired."
            ),
            403: OpenApiResponse(
                description="Requesting user is not the owner of the comment."
            ),
            404: OpenApiResponse(description="Comment for given id not found."),
        },
    ),
)
