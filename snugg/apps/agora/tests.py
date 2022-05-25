from urllib.parse import urlencode

import factory
from django.urls import reverse
from factory.django import DjangoModelFactory
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from snugg.apps.user.tests import UserFactory

from .models import Lecture, Post, Semester

fake = Faker()


class LectureFactory(DjangoModelFactory):
    class Meta:
        model = Lecture

    lecture = factory.Faker("name")
    lecture_id = factory.Faker("pyfoat")
    instructor = factory.Faker("name")
    # semesters =


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    lecture = factory.SubFactory(LectureFactory)
    writer = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=4)
    content = factory.Faker("text")


class SemesterFactory(DjangoModelFactory):
    class Meta:
        model = Semester

    year = factory.Faker("year")
    # season =


class LectureAPITestCase(APITestCase):
    """
    Helper methods for Lecture retrieve/list API request included.
    """

    def retrieve_lecture(self, pk):
        return self.client.get(reverse("agora-lecture-detail"), args=[pk])

    def list_lecture(self, **params):
        return self.client.get(f"{reverse('agora-lecture-list')}?{urlencode(params)}")


class PostAPITestCase(APITestCase):
    """
    Helper methods for Post CRUD API request included.
    """

    def create_post(self, data):
        return self.client.post(reverse("agora-post-list"), data=data)

    def retrieve_post(self, pk):
        return self.client.get(reverse("agora-post-detail", args=[pk]))

    def list_post(self, **params):
        return self.client.get(f"{reverse('agora-post-list')}?{urlencode(params)}")

    def update_post(self, pk, data):
        return self.client.put(reverse("agora-post-detail", args=[pk]), data)

    def partial_update_post(self, pk, data):
        return self.client.patch(reverse("agora-post-detail", args=[pk]), data)

    def destroy_post(self, pk):
        return self.client.delete(reverse("agora-post-detail", args=[pk]))
