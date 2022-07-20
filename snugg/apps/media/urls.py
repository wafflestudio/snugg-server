from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import PresignedURLViewSet

router = SimpleRouter()

router.register("media/presigned", PresignedURLViewSet, basename="media-presigned")

urlpatterns = (path("", include(router.urls)),)
