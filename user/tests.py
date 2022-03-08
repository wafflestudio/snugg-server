from django.test import TestCase
from django.db import transaction
from factory.django import DjangoModelFactory
import factory
from .models import User
from rest_framework import status


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
        response = self.client.post('/user/signup/', data=self.post_data)
        new_user = User.objects.filter(email=self.post_data['email'])[0]

        self.assertEqual(new_user.email, self.post_data.get('email'))
        self.assertEqual(new_user.username, self.post_data.get('username'))
        self.assertEqual(new_user.birth_date.strftime('%Y-%m-%d'), self.post_data.get('birth_date'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)