from django.test import TestCase
from django.db import transaction
from factory.django import DjangoModelFactory
import factory
from .models import User
from rest_framework import status

# Create your tests here.
class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@gmail.com')
    password = '1234'

    # @classmethod
    # def create(cls, **kwargs):
    #     User.objects.create(**kwargs)


class SignUpTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post_data = {
            'email': 'waffle@test.com',
            'username': 'steve',
            'password': 'password',
            'birth_date': '1999-03-21'
        }

    def testSignUp(self):
        with transaction.atomic():
            response = self.client.post('/user/signup/', data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)