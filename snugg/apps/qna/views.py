from rest_framework.viewsets import ModelViewSet

from .models import Post
from .serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects
    serializer_class = PostSerializer

    # TODO: object level permissions for Update, Partial Update, Destroy
    # TODO: tagging
    # TODO: handle serializer relations for writer, accepted answer, tags, etc. (ref: https://www.django-rest-framework.org/api-guide/relations/)
    # TODO: query optimization
