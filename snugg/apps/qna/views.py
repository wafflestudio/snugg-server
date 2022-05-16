from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import CursorPagination
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from ...s3 import create_presigned_post, delete_object
from .models import Answer, Post
from .schemas import post_viewset_schema
from .serializers import AnswerSerializer, PostSerializer
from ...settings import MEDIA_ROOT


class PostFilter(filters.FilterSet):
    field = filters.CharFilter(field_name="field__name", lookup_expr="iexact")
    tag = filters.CharFilter(field_name="tags__name", lookup_expr="iexact")

    class Meta:
        model = Post
        fields = ("writer",)


class PostPagination(CursorPagination):
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
            }
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
    ordering = "-created_at"
    pagination_class = PostPagination

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        path = "/".join([MEDIA_ROOT, "images", "answer", str(response.data["pk"]), ""])
        response.data["presigned"] = {
            "url": "https://snugg-s3.s3.amazonaws.com/",
            "fields": {
                "key": path,
            }
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
