import factory
from factory.django import DjangoModelFactory
from faker import Faker

from snugg.apps.user.tests import UserFactory

from ..models import Answer, Comment, Field, Post

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

    post = factory.SubFactory(PostFactory)
    writer = factory.SubFactory(UserFactory)
    content = factory.Faker("text")


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    writer = factory.SubFactory(UserFactory)
    content = factory.Faker("text")
    content_object = factory.SubFactory(PostFactory)
