from random import choice
from urllib.parse import urlencode

import factory
from django.urls import reverse
from factory.django import DjangoModelFactory
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from snugg.apps.user.tests import UserFactory

from .models import Answer, Field, Post

fake = Faker()


class FieldFactory(DjangoModelFactory):
    class Meta:
        model = Field

    name = factory.Faker("word")


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    # TODO: comments
    field = factory.SubFactory(FieldFactory)
    writer = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=4)
    content = factory.Faker("text")

    @factory.post_generation
    def tags(self, create, extracted):
        if not create:
            return

        if extracted:
            self.tags.add(*extracted)
        else:
            self.tags.add(*fake.words())


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer

    # TODO: comments
    post = factory.SubFactory(PostFactory)
    writer = factory.SubFactory(UserFactory)
    content = factory.Faker("text")


class PostAPITestCase(APITestCase):
    """
    Post CRUD API request methods included.
    """

    def create_post(self, data):
        return self.client.post(reverse("post-list"), data=data)

    def retrieve_post(self, pk):
        return self.client.get(reverse("post-detail", args=[pk]))

    def list_post(self, **params):
        return self.client.get(f"{reverse('post-list')}?{urlencode(params)}")

    def update_post(self, pk, data):
        return self.client.put(reverse("post-detail", args=[pk]), data)

    def partial_update_post(self, pk, data):
        return self.client.patch(reverse("post-detail", args=[pk]), data)

    def destroy_post(self, pk):
        return self.client.delete(reverse("post-detail", args=[pk]))
