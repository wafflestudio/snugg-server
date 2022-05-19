from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    AnswerViewSet,
    CommentAnswerViewSet,
    CommentPostViewSet,
    CommentViewSet,
    PostViewSet,
    ReplyViewSet,
)

router = SimpleRouter()
router.register("qna/posts", PostViewSet, basename="post")
router.register("qna/comments/post", CommentPostViewSet, basename="post-comment")
router.register("qna/comments/answer", CommentAnswerViewSet, basename="answer-comment")
router.register("qna/comments/reply", ReplyViewSet, basename="reply")
router.register("qna/comments", CommentViewSet, basename="comment")


router.register("qna/answers", AnswerViewSet, basename="answer")

urlpatterns = (path("", include(router.urls)),)
