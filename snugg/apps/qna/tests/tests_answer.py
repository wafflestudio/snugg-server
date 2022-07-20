from urllib.parse import urlencode

from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Answer, Post
from .factories import PostFactory, UserFactory

fake = Faker()


class AnswerAPITestCase(APITestCase):
    """
    Answer CRUD API request methods included.
    """

    def create_answer(self, data):
        return self.client.post(reverse("answer-list"), data=data)

    def retrieve_answer(self, pk):
        return self.client.get(reverse("answer-detail", args=[pk]))

    def list_answer(self, **params):
        return self.client.get(f"{reverse('answer-list')}?{urlencode(params)}")

    def update_answer(self, pk, data):
        return self.client.put(reverse("answer-detail", args=[pk]), data)

    def partial_update_answer(self, pk, data):
        return self.client.patch(reverse("answer-detail", args=[pk]), data)

    def destroy_answer(self, pk):
        return self.client.delete(reverse("answer-detail", args=[pk]))


class AnswerCreateTests(AnswerAPITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserFactory()
        cls.post = PostFactory(writer=UserFactory())

        cls.data = {
            "post": cls.post.pk,
            "content": fake.text(),
        }

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_answer_create(self):
        response = self.create_answer(self.data)
        answer = Answer.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("writer").get("pk"), self.user.pk)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(answer.writer, self.user)
        self.assertEqual(answer.content, self.data.get("content"))

    def test_answer_create_accepted_already(self):
        response = self.create_answer(self.data)

        self.post.accepted_answer = Answer.objects.first()
        self.post.save()

        response = self.create_answer(self.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
