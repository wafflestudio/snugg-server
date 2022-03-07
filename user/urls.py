from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserSignUpViewSet

router = SimpleRouter()
router.register(r'signup', UserSignUpViewSet, basename='signup')

urlpatterns = (
    path('', include(router.urls)),
)