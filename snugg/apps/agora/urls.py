from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import LectureViewSet

router = SimpleRouter()
router.register("agora/lectures", LectureViewSet, basename="post")

urlpatterns = (path("", include(router.urls)),)
