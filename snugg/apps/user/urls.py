from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserAccountViewSet

router = SimpleRouter()
router.register("auth", UserAccountViewSet, basename="user-account")

urlpatterns = (path("", include(router.urls)),)
