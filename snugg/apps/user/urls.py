from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserAccountViewSet

router = SimpleRouter()
router.register(r"", UserAccountViewSet, basename="signup")

urlpatterns = (path("", include(router.urls)),)
