from django.contrib.contenttypes.models import ContentType
from django.http.request import QueryDict
from django_filters import rest_framework as filters
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from ...s3 import create_presigned_post, delete_object
from ...settings import MEDIA_ROOT
from .models import Answer, Comment, Post
from .schemas import (
    comment_create_view,
    comment_list_view,
    comment_viewset_schema,
    post_viewset_schema,
)
from .serializers import (
    AnswerSerializer,
    CommentAnswerSerializer,
    CommentPostSerializer,
    CommentSerializer,
    PostSerializer,
    ReplySerializer,
)


class PostFilter(filters.FilterSet):
    field = filters.CharFilter(field_name="field__name", lookup_expr="iexact")
    tag = filters.CharFilter(field_name="tags__name", lookup_expr="iexact")

    class Meta:
        model = Post
        fields = ("writer",)


class PostPagination(CursorPagination):
    page_size = 10
    page_size_query_param = "page_size"


class CommentPagination(CursorPagination):
    page_size = 10
    page_size_query_param = "page_size"


@post_viewset_schema
class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related("field", "writer").prefetch_related("tags")
    serializer_class = PostSerializer
    filter_backends = (
        OrderingFilter,
        SearchFilter,
        filters.DjangoFilterBackend,
    )
    filterset_class = PostFilter
    ordering_fields = (
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "content",
    )
    ordering = "-created_at"
    pagination_class = PostPagination

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        path = "/".join([MEDIA_ROOT, "images", "post", str(response.data["pk"]), ""])
        response.data["presigned"] = {
            "url": "https://snugg-s3.s3.amazonaws.com/",
            "fields": {
                "key": path,
            },
        }
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        path = "/".join([MEDIA_ROOT, "images", "post", str(response.data["pk"]), ""])
        response.data["presigned"] = create_presigned_post(
            path, conditions=[("acl", "public-read")]
        )
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        partial = kwargs.pop("partial", False)
        pk = kwargs.get("pk")
        path = "/".join([MEDIA_ROOT, "images", "post", str(pk), ""])
        if not partial:
            delete_object(prefix=path)
        response.data["presigned"] = create_presigned_post(
            path, conditions=[("acl", "public-read")]
        )
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        pk = kwargs.get("pk")
        path = "/".join([MEDIA_ROOT, "images", "post", str(pk), ""])
        delete_object(prefix=path)
        return response


class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.select_related("writer")
    serializer_class = AnswerSerializer
    filter_backends = (
        OrderingFilter,
        filters.DjangoFilterBackend,
    )
    filterset_fields = ("writer",)
    ordering_fields = (
        "created_at",
        "updated_at",
    )
    filterset_fields = ["post"]
    ordering = "-created_at"
    pagination_class = PostPagination

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        path = "/".join([MEDIA_ROOT, "images", "answer", str(response.data["pk"]), ""])
        response.data["presigned"] = {
            "url": "https://snugg-s3.s3.amazonaws.com/",
            "fields": {
                "key": path,
            },
        }
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        path = "/".join([MEDIA_ROOT, "images", "answer", str(response.data["pk"]), ""])
        response.data["presigned"] = create_presigned_post(
            path, conditions=[("acl", "public-read")]
        )
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        partial = kwargs.pop("partial", False)
        pk = kwargs.get("pk")
        path = "/".join([MEDIA_ROOT, "images", "answer", str(pk), ""])
        if not partial:
            delete_object(prefix=path)
        response.data["presigned"] = create_presigned_post(
            path, conditions=[("acl", "public-read")]
        )
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        pk = kwargs.get("pk")
        path = "/".join([MEDIA_ROOT, "images", "answer", str(pk), ""])
        delete_object(prefix=path)
        return response


@comment_viewset_schema
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.select_related("writer")
    serializer_class = CommentSerializer
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend)
    ordering_fields = ("created_at", "updated_at")
    ordering = "-created_at"
    pagination_class = CommentPagination

    @comment_list_view
    def list(self, request, *args, **kwargs):
        answer = request.query_params.get("answer", "")
        comment = request.query_params.get("comment", "")
        post = request.query_params.get("post", "")
        if answer:
            if answer.isnumeric():
                answer = int(answer)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not Answer.objects.filter(id=answer).exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            self.queryset = self.queryset.filter(
                content_type=ContentType.objects.get_for_model(Answer),
                object_id=answer,
            )
        elif comment:
            if comment.isnumeric():
                comment = int(comment)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not Comment.objects.filter(id=comment).exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            self.queryset = self.queryset.filter(
                content_type=ContentType.objects.get_for_model(Comment),
                object_id=comment,
            )
        elif post:
            if post.isnumeric():
                post = int(post)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not Post.objects.filter(id=post).exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            self.queryset = self.queryset.filter(
                content_type=ContentType.objects.get_for_model(Post),
                object_id=post,
            )

        return super().list(self, request, *args, **kwargs)

    @comment_create_view
    def create(self, request, *args, **kwargs):
        answer = request.query_params.get("answer", "")
        comment = request.query_params.get("comment", "")
        post = request.query_params.get("post", "")
        data = request.data.copy()
        if answer:
            if answer.isnumeric():
                answer = int(answer)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not Answer.objects.filter(id=answer).exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            data["object_id"] = answer
            data["content_type"] = ContentType.objects.get_for_model(Answer)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            super().perform_create(serializer)
            headers = super().get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        elif comment:
            if comment.isnumeric():
                comment = int(comment)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not Comment.objects.filter(id=comment).exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            data["object_id"] = comment
            data["content_type"] = ContentType.objects.get_for_model(Comment)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            super().perform_create(serializer)
            headers = super().get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        elif post:
            if post.isnumeric():
                post = int(post)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if not Post.objects.filter(id=post).exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            data["object_id"] = post
            data["content_type"] = ContentType.objects.get_for_model(Post)
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            super().perform_create(serializer)
            headers = super().get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
