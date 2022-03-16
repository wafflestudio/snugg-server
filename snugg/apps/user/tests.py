import factory
from django.test import TestCase
from factory.django import DjangoModelFactory
from faker import Faker
from rest_framework import status

from .models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@gmail.com")
    # username = factory.Faker("user_name")
    # email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", fake.password())
    birth_date = factory.Faker("date")
    is_active = True


class SignUpTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # cls.user_data = {
        #     "email": "waffle@test.com",
        #     "username": "steve",
        #     "password": "password",
        #     "birth_date": "1999-03-21",
        # }
        fake = Faker()
        cls.user_data = {
            "email": fake.email(),
            "username": fake.user_name(),
            "password": fake.password(),
            "birth_date": fake.date(),
        }

    def test_signup(self):
        response = self.client.post("/auth/signup/", data=self.user_data)
        user = User.objects.first()

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(
            response.data.get("user").get("email"), self.user_data.get("email")
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, self.user_data.get("email"))
        self.assertEqual(user.username, self.user_data.get("username"))
        self.assertEqual(
            user.birth_date.strftime("%Y-%m-%d"), self.user_data.get("birth_date")
        )

    def test_signup_email_duplicate(self):
        self.client.post("/auth/signup/", data=self.user_data)
        data = self.user_data.copy()
        data.update({"username": "jason"})
        response = self.client.post("/auth/signup/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_permissions(self):
        data = self.user_data.copy()
        data.update(
            {
                "is_staff": True,
                "is_superuser": True,
                "is_active": False,
                "is_admin": True,
            }
        )
        response = self.client.post("/auth/signup/", data=data)
        user = User.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_admin, False)


class SigninTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        fake = Faker()
        cls.user_data = {
            "email": fake.email(),
            "password": fake.password(),
        }
        cls.user = UserFactory(**cls.user_data)

    def test_signin(self):
        response = self.client.post("/auth/signin/", data=self.user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signin_email_wrong(self):
        data = self.user_data.copy()
        data.update({"email": data.get("email") + "a"})
        response = self.client.post("/auth/signin/", data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_signin_password_wrong(self):
        data = self.user_data.copy()
        data.update({"password": data.get("password") + "a"})
        response = self.client.post("/auth/signin/", data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
