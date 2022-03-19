from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import PostViewSet

router = SimpleRouter()
router.register("qna/posts", PostViewSet, basename="post")

urlpatterns = (path("", include(router.urls)),)
