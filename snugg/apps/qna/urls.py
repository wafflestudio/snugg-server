from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AnswerViewSet, PostViewSet

router = SimpleRouter()
router.register("qna/posts", PostViewSet, basename="qna-post")
router.register("qna/answers", AnswerViewSet, basename="answer")

urlpatterns = (path("", include(router.urls)),)
