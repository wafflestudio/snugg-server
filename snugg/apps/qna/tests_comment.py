from random import choice
from urllib.parse import urlencode

import factory
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from factory.django import DjangoModelFactory
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from snugg.apps.qna.tests import FieldFactory, PostFactory
from snugg.apps.qna.tests_answer import AnswerAPITestCase, AnswerFactory
from snugg.apps.user.tests import UserFactory

from .models import Answer, Comment, Field, Post

fake = Faker()


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    object_id = 1
    content_type = ContentType.objects.get_for_model(Answer)
    writer = factory.SubFactory(UserFactory)
    content = factory.Faker("text")


class CommentAPITestCase(AnswerAPITestCase):
    """
    Comment CRUD API request methods included.
    """

    def create_comment_post(self, data, **params):
        return self.client.post(
            f"{reverse('post-comment-list')}?{urlencode(params)}", data=data
        )

    def create_comment_answer(self, data, **params):
        return self.client.post(
            f"{reverse('answer-comment-list')}?{urlencode(params)}", data=data
        )

    def create_reply(self, data, **params):
        return self.client.post(
            f"{reverse('reply-list')}?{urlencode(params)}", data=data
        )

    def retrieve_comment(self, pk):
        return self.client.get(reverse("comment-detail", args=[pk]))

    def list_comment(self, **params):
        return self.client.get(f"{reverse('comment-list')}?{urlencode(params)}")

    def list_comment_post(self, **params):
        return self.client.get(f"{reverse('post-comment-list')}?{urlencode(params)}")

    def list_comment_answer(self, **params):
        return self.client.get(f"{reverse('answer-comment-list')}?{urlencode(params)}")

    def list_reply(self, **params):
        return self.client.get(f"{reverse('reply-list')}?{urlencode(params)}")

    def update_comment(self, pk, data):
        return self.client.put(reverse("comment-detail", args=[pk]), data)

    def partial_update_comment(self, pk, data):
        return self.client.patch(reverse("comment-detail", args=[pk]), data)

    def destroy_comment(self, pk):
        return self.client.delete(reverse("comment-detail", args=[pk]))


class CommentCreateTests(CommentAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = PostFactory()
        cls.answer = AnswerFactory()
        cls.user = UserFactory()
        cls.comment = CommentFactory()

        cls.data = {
            "content": fake.text(),
        }

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_comment_post_create(self):
        response = self.create_comment_post(self.data, id=self.post.id)
        comment = Comment.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("writer").get("pk"), self.user.pk)
        self.assertEqual(response.data.get("replies_count"), 0)

        self.assertEqual(comment.writer, self.user)
        self.assertEqual(comment.content, self.data.get("content"))
        self.assertEqual(comment.content_type, ContentType.objects.get_for_model(Post))
        self.assertEqual(comment.object_id, self.post.id)

    def test_comment_post_create_id_wrong(self):
        response = self.create_comment_post(self.data, id=100)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_comment_answer_create(self):
        response = self.create_comment_answer(self.data, id=self.answer.id)
        comment = Comment.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("writer").get("pk"), self.user.pk)
        self.assertEqual(response.data.get("replies_count"), 0)

        self.assertEqual(comment.writer, self.user)
        self.assertEqual(comment.content, self.data.get("content"))
        self.assertEqual(
            comment.content_type, ContentType.objects.get_for_model(Answer)
        )
        self.assertEqual(comment.object_id, self.answer.id)

    def test_reply_create(self):
        response = self.create_reply(self.data, id=self.comment.id)
        comment = Comment.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("writer").get("pk"), self.user.pk)

        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(comment.writer, self.user)
        self.assertEqual(comment.content, self.data.get("content"))
        self.assertEqual(
            comment.content_type, ContentType.objects.get_for_model(Comment)
        )
        self.assertEqual(comment.object_id, self.comment.id)


#
# class CommentReadTests(CommentAPITestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.comments = CommentFactory.create_batch(25)
#
#