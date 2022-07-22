from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import LectureViewSet, StoryViewSet

router = SimpleRouter()
router.register("agora/lectures", LectureViewSet, basename="agora-lecture")
router.register("agora/storys", StoryViewSet, basename="agora-story")

urlpatterns = (path("", include(router.urls)),)
