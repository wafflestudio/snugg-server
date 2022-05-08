from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import LectureViewSet, PostViewSet

router = SimpleRouter()
router.register("agora/lectures", LectureViewSet, basename="agora-lecture")
router.register("agora/posts", PostViewSet, basename="agora-post")

urlpatterns = (path("", include(router.urls)),)
