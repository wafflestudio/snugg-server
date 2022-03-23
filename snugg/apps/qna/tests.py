import json
from random import choice

import factory
from django.test import TestCase
from factory.django import DjangoModelFactory
from faker import Faker
from rest_framework import status
from snugg.apps.qna.views import PostPagination
from snugg.apps.user.tests import UserFactory
from snugg.tokens import jwt_token_of

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
    # factory.RelatedFactory for accepted_answer?
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
