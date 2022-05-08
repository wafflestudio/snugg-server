from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Lecture, Post
from .serializers import LectureSerializer, PostSerializer


class LectureFilter(filters.FilterSet):
    university = filters.CharFilter(
        field_name="university__name", lookup_expr="icontains"
    )
    college = filters.CharFilter(field_name="college__name", lookup_expr="icontains")
    major = filters.CharFilter(field_name="major__name", lookup_expr="icontains")
    year = filters.NumberFilter(field_name="semesters__year", distinct=True)
    season = filters.NumberFilter(field_name="semesters__season", distinct=True)


class LecturePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class LectureViewSet(ReadOnlyModelViewSet):
    queryset = Lecture.objects.select_related(
        "university", "college", "major"
    ).prefetch_related("semesters")
    serializer_class = LectureSerializer
    filter_backends = (
        OrderingFilter,
        SearchFilter,
        filters.DjangoFilterBackend,
    )
    filterset_class = LectureFilter
    ordering_fields = ("name",)
    ordering = "name"
    search_fields = ("name", "lecture_id", "instructor")
    pagination_class = LecturePagination


class PostPagination(CursorPagination):
    page_size = 10
    page_size_query_param = "page_size"


class PostViewSet(ModelViewSet):
    queryset = Post.objects.select_related(
        "lecture", "writer", "lecture__university", "lecture__college", "lecture__major"
    ).prefetch_related("lecture__semesters")
    serializer_class = PostSerializer
    filter_backends = (
        OrderingFilter,
        SearchFilter,
        filters.DjangoFilterBackend,
    )
    filterset_fields = (
        "lecture",
        "writer",
    )
    ordering_fields = (
        "created_at",
        "updated_at",
    )
    ordering = "-created_at"
    search_fields = (
        "title",
        "content",
    )
    pagination_class = PostPagination
