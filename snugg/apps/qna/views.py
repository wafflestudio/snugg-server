from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import CursorPagination
from rest_framework.viewsets import ModelViewSet

from .models import Post
from .schemas import post_viewset_schema
from .serializers import PostSerializer


class PostFilter(filters.FilterSet):
    field = filters.CharFilter(field_name="field__name", lookup_expr="iexact")
    tag = filters.CharFilter(field_name="tags__name", lookup_expr="iexact")


class PostPagination(CursorPagination):
    page_size = 10


@post_viewset_schema
class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related("field", "writer").prefetch_related("tags")
    serializer_class = PostSerializer
    filter_backends = (
        OrderingFilter,
        filters.DjangoFilterBackend,
    )
    filterset_class = PostFilter
    ordering_fields = (
        "pk",
        "writer",
        "title",
        "created_at",
        "updated_at",
    )
    ordering = "-updated_at"
    pagination_class = PostPagination

    # TODO: test scipts
