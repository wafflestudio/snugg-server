from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet

from .models import Post
from .serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = (
        "pk",
        "writer",
        "title",
        "created_at",
        "updated_at",
    )
    ordering = "-updated_at"

    # TODO: filter by tags
    # TODO: handle serializer relations for writer, accepted answer, tags, etc. (ref: https://www.django-rest-framework.org/api-guide/relations/)
    # TODO: test scipts
    # TODO: list action ordering
    # TODO: query optimization
