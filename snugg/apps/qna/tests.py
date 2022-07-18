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
        return self.client.post(reverse("qna-post-list"), data=data)

    def retrieve_post(self, pk):
        return self.client.get(reverse("qna-post-detail", args=[pk]))

    def list_post(self, **params):
        return self.client.get(f"{reverse('qna-post-list')}?{urlencode(params)}")

    def update_post(self, pk, data):
        return self.client.put(reverse("qna-post-detail", args=[pk]), data)

    def partial_update_post(self, pk, data):
        return self.client.patch(reverse("qna-post-detail", args=[pk]), data)

    def destroy_post(self, pk):
        return self.client.delete(reverse("qna-post-detail", args=[pk]))


class PostCreateTests(PostAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.data = {
            "field": FieldFactory().name,
            "title": fake.sentence(nb_words=4),
            "content": fake.text(),
            "tags": fake.words(),
        }

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_post_create(self):
        response = self.create_post(self.data)
        post = Post.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("writer").get("pk"), self.user.pk)

        data = {**self.data, "tags": sorted(self.data.get("tags"))}
        response.data.update({"tags": sorted(response.data.get("tags"))})
        self.assertEqual(response.data, {**response.data, **data})

        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.field.name, self.data.get("field"))
        self.assertEqual(post.writer, self.user)
        self.assertEqual(post.title, self.data.get("title"))
        self.assertEqual(post.content, self.data.get("content"))

        obj_tags = sorted([tag.name for tag in list(post.tags.all())])
        self.assertListEqual(obj_tags, data.get("tags"))

    def test_post_create_writer(self):
        data = {**self.data, "writer": UserFactory().pk}
        response = self.create_post(data)
        post = Post.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("writer").get("pk"), self.user.pk)
        self.assertEqual(post.writer, self.user)

    def test_post_create_field_case_insensitive(self):
        crazy_field_name = "".join(
            choice((str.upper, str.lower))(c) for c in self.data.get("field")
        )
        data = {**self.data, "field": crazy_field_name}
        response = self.create_post(data)
        post = Post.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data.get("field").casefold(), data.get("field").casefold()
        )
        self.assertEqual(post.field.name.casefold(), data.get("field").casefold())

    def test_post_create_field_wrong(self):
        data = {**self.data, "field": fake.word()}
        response = self.create_post(data)

        self.assertContains(response, "field", None, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_create_title_too_long(self):
        data = {**self.data, "title": fake.text()}
        response = self.create_post(data)

        self.assertContains(response, "title", None, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_create_accepted_answer_wrong(self):
        data = {**self.data, "accepted_answer": 1}
        response = self.create_post(data)

        self.assertContains(
            response, "accepted_answer", None, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(Post.objects.count(), 0)

        answer = AnswerFactory()
        data.update({"accepted_answer": answer.pk})
        response = self.create_post(data)

        self.assertContains(
            response, "accepted_answer", None, status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(Post.objects.count(), 1)

    def test_post_create_data_insufficient(self):
        data = self.data.copy()
        data.pop("field")
        response = self.create_post(data)

        self.assertContains(response, "field", None, status.HTTP_400_BAD_REQUEST)

        data = self.data.copy()
        data.pop("title")
        response = self.create_post(data)

        self.assertContains(response, "title", None, status.HTTP_400_BAD_REQUEST)

        data = self.data.copy()
        data.pop("content")
        response = self.create_post(data)

        self.assertContains(response, "content", None, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_create_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.create_post(self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)


class PostReadTests(PostAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.posts = PostFactory.create_batch(25)

    def test_post_retrieve(self):
        post = choice(self.posts)
        response = self.retrieve_post(post.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("field"), post.field.name)
        self.assertEqual(response.data.get("writer").get("username"), post.writer.username)
        self.assertEqual(response.data.get("title"), post.title)
        self.assertEqual(response.data.get("content"), post.content)

        res_tags = sorted(response.data.get("tags"))
        obj_tags = sorted([tag.name for tag in list(post.tags.all())])
        self.assertEqual(res_tags, obj_tags)

    def test_post_retrieve_not_found(self):
        response = self.retrieve_post(999)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_list(self):
        response = self.list_post()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_list_filter(self):
        post = choice(self.posts)
        field_name = post.field.name
        response = self.list_post(field=field_name)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data.get("results")), 1)

        for result in response.data.get("results"):
            self.assertEqual(result.get("field"), field_name)

        post = choice(self.posts)
        tag_name = choice(post.tags.all()).name
        response = self.list_post(tag=tag_name.upper())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data.get("results")), 1)

        for result in response.data.get("results"):
            self.assertIn(tag_name, result.get("tags"))

        post = choice(self.posts)
        writer_pk = post.writer.pk
        response = self.list_post(writer=writer_pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data.get("results")), 1)

        for result in response.data.get("results"):
            self.assertEqual(result.get("writer").get("pk"), writer_pk)

    def test_post_list_ordering(self):
        response = self.list_post(ordering="-created_at")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results")
        for i in range(1, len(results)):
            results[i - 1].get("created_at") > results[i].get("created_at")

        response = self.list_post(ordering="updated_at")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get("results")
        for i in range(1, len(results)):
            results[i - 1].get("updated_at") < results[i].get("updated_at")

    def test_post_list_pagination(self):
        response = self.list_post(page_size=10)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 10)

        next_url = response.data.get("next")
        response = self.client.get(next_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 10)

        next_url = response.data.get("next")
        response = self.client.get(next_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")), 5)


class PostUpdateTests(PostAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.post = PostFactory(writer=cls.user)

        cls.data = {
            "field": FieldFactory().name,
            "title": fake.sentence(nb_words=4),
            "content": fake.text(),
            "accepted_answer": AnswerFactory(post=cls.post).pk,
            "tags": fake.words(),
        }

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_post_update(self):
        response = self.update_post(self.post.pk, self.data)
        self.post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("writer").get("pk"), self.user.pk)

        data = {**self.data, "tags": sorted(self.data.get("tags"))}
        response.data.update({"tags": sorted(response.data.get("tags"))})
        self.assertEqual(response.data, {**response.data, **data})

        self.assertEqual(self.post.field.name, data.get("field"))
        self.assertEqual(self.post.writer, self.user)
        self.assertEqual(self.post.title, data.get("title"))
        self.assertEqual(self.post.content, data.get("content"))
        self.assertEqual(self.post.accepted_answer.pk, data.get("accepted_answer"))

        obj_tags = sorted([tag.name for tag in list(self.post.tags.all())])
        self.assertListEqual(obj_tags, data.get("tags"))

    def test_post_update_writer(self):
        data = {**self.data, "writer": UserFactory().pk}
        response = self.update_post(self.post.pk, data)
        self.post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("writer").get("pk"), self.user.pk)
        self.assertEqual(self.post.writer, self.user)

    def test_post_update_field_wrong(self):
        data = {**self.data, "field": fake.word()}
        response = self.update_post(self.post.pk, data)
        self.post.refresh_from_db()

        self.assertContains(response, "field", None, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.post.field.name, data.get("field"))
        self.assertNotEqual(self.post.title, data.get("title"))

    def test_post_update_title_too_long(self):
        data = {**self.data, "title": fake.text()}
        response = self.update_post(self.post.pk, data)
        self.post.refresh_from_db()

        self.assertContains(response, "title", None, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.post.title, data.get("title"))
        self.assertNotEqual(self.post.content, data.get("content"))

    def test_post_update_accepted_answer_wrong(self):
        data = {**self.data, "accepted_answer": AnswerFactory().pk}
        response = self.update_post(self.post.pk, data)
        self.post.refresh_from_db()

        self.assertContains(
            response, "accepted_answer", None, status.HTTP_400_BAD_REQUEST
        )
        self.assertIsNone(self.post.accepted_answer)
        self.assertNotEqual(self.post.title, data.get("title"))

    def test_post_update_data_insufficient(self):
        data = self.data.copy()
        data.pop("title")
        response = self.update_post(self.post.pk, data)
        self.post.refresh_from_db()

        self.assertContains(response, "title", None, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(self.post.title)
        self.assertNotEqual(self.post.title, "")
        self.assertNotEqual(self.post.content, data.get("content"))

    def test_post_update_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.update_post(self.post.pk, self.data)
        self.post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(self.post.title, self.data.get("title"))

    def test_post_update_permission_denied(self):
        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)
        response = self.update_post(self.post.pk, self.data)
        self.post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.post.title, self.data.get("title"))
        self.assertNotEqual(self.post.writer, new_user)

    def test_post_update_not_found(self):
        response = self.update_post(999, self.data)
        self.post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(self.post.title, self.data.get("title"))

    def test_post_partial_update(self):
        data = self.data.copy()
        data.pop("accepted_answer")
        data.pop("title")
        response = self.partial_update_post(self.post.pk, data)
        self.post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("writer").get("pk"), self.user.pk)

        data = {**data, "tags": sorted(data.get("tags"))}
        response.data.update({"tags": sorted(response.data.get("tags"))})
        self.assertEqual(response.data, {**response.data, **data})

        self.assertEqual(self.post.field.name, data.get("field"))
        self.assertEqual(self.post.writer, self.user)
        self.assertNotEqual(self.post.title, self.data.get("title"))
        self.assertEqual(self.post.content, data.get("content"))
        self.assertIsNone(self.post.accepted_answer)

        obj_tags = sorted([tag.name for tag in list(self.post.tags.all())])
        self.assertListEqual(obj_tags, data.get("tags"))

    def test_post_partial_update_writer(self):
        data = {"writer": UserFactory().pk}
        response = self.partial_update_post(self.post.pk, data)
        self.post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("writer").get("pk"), self.user.pk)
        self.assertEqual(self.post.writer, self.user)

    def test_post_partial_update_field_wrong(self):
        data = {"field": fake.word()}
        response = self.partial_update_post(self.post.pk, data)
        self.post.refresh_from_db()

        self.assertContains(response, "field", None, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.post.field.name, data.get("field"))

    def test_post_partial_update_title_too_long(self):
        data = {"title": fake.text()}
        response = self.partial_update_post(self.post.pk, data)
        self.post.refresh_from_db()

        self.assertContains(response, "title", None, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(self.post.title, data.get("title"))

    def test_post_partial_update_accepted_answer_wrong(self):
        data = {"accepted_answer": AnswerFactory().pk}
        response = self.partial_update_post(self.post.pk, data)
        self.post.refresh_from_db()

        self.assertContains(
            response, "accepted_answer", None, status.HTTP_400_BAD_REQUEST
        )
        self.assertIsNone(self.post.accepted_answer)

    def test_post_partial_update_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.partial_update_post(self.post.pk, self.data)
        self.post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotEqual(self.post.title, self.data.get("title"))

    def test_post_partial_update_permission_denied(self):
        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)
        response = self.update_post(self.post.pk, self.data)
        self.post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.post.title, self.data.get("title"))
        self.assertNotEqual(self.post.writer, new_user)

    def test_post_partial_update_not_found(self):
        response = self.partial_update_post(999, self.data)
        self.post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(self.post.title, self.data.get("title"))


class PostDeleteTests(PostAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.post = PostFactory(writer=cls.user)

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_post_destroy(self):
        response = self.destroy_post(self.post.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertRaises(Post.DoesNotExist, lambda: Post.objects.get(pk=self.post.pk))
        self.assertEqual(Post.objects.count(), 0)

    def test_post_destroy_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.destroy_post(self.post.pk)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 1)

    def test_post_destroy_permission_denied(self):
        self.client.force_authenticate(user=UserFactory())
        response = self.destroy_post(self.post.pk)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)

    def test_post_destroy_not_found(self):
        response = self.destroy_post(999)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Post.objects.count(), 1)
