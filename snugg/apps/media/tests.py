from django.urls import reverse
from django.utils.text import slugify
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from snugg.apps.user.tests import UserFactory

from .models import Directory

fake = Faker()


class PresignedAPITestCase(APITestCase):
    """
    Presigned API request methods included.
    """

    def create_presigned(self, data):
        return self.client.post(reverse("media-presigned-list"), data=data)


class PresignedCreateTests(PresignedAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.data = {"filenames": fake.words(nb=5, unique=True)}

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_presigned_create(self):
        response = self.create_presigned(self.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("uploader").get("pk"), self.user.pk)

        filenames_slug = [slugify(filename) for filename in self.data.get("filenames")]
        self.assertListEqual(filenames_slug, response.data.get("filenames"))

        self.assertEqual(
            len(self.data.get("filenames")), len(response.data.get("presigned_posts"))
        )

    def test_presigned_empty_filenames(self):
        data = self.data.update({"filenames": []})
        response = self.create_presigned(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_presigned_create_unauthorized(self):
        self.client.force_authenticate(user=None)
        response = self.create_presigned(self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Directory.objects.count(), 0)
