import factory
from django.test import TestCase
from django.urls import reverse
from factory.django import DjangoModelFactory
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from snugg.tokens import jwt_token_of

from .models import User

fake = Faker()


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


class AuthAPITestCase(APITestCase):
    """
    Auth API request methods included.
    """

    def signup(self, data):
        return self.client.post(reverse("user-account-signup"), data=data)

    def signin(self, data):
        return self.client.post(reverse("user-account-signin"), data=data)

    def signout(self, data):
        return self.client.post(reverse("user-account-signout"), data=data)


class SignUpTests(AuthAPITestCase):
    @classmethod
    def setUpTestData(cls):
        # cls.user_data = {
        #     "email": "waffle@test.com",
        #     "username": "steve",
        #     "password": "password",
        #     "birth_date": "1999-03-21",
        # }
        cls.data = {
            "email": fake.email(),
            "username": fake.user_name(),
            "password": fake.password(),
            "birth_date": fake.date(),
        }

    def test_signup(self):
        response = self.signup(self.data)
        user = User.objects.first()

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data.get("user").get("email"), self.data.get("email"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, self.data.get("email"))
        self.assertEqual(user.username, self.data.get("username"))
        self.assertEqual(
            user.birth_date.strftime("%Y-%m-%d"), self.data.get("birth_date")
        )

    def test_signup_email_duplicate(self):
        self.client.post("/auth/signup/", data=self.data)
        data = {**self.data, "username": fake.name()}
        response = self.signup(data)

        self.assertContains(response, "email", None, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_data_insufficient(self):
        data = self.data.copy()
        data.pop("email")
        response = self.signup(data)

        self.assertContains(response, "email", None, status.HTTP_400_BAD_REQUEST)

        data = self.data.copy()
        data["password"] = ""
        response = self.signup(data)

        self.assertContains(response, "password", None, status.HTTP_400_BAD_REQUEST)

    def test_signup_permissions(self):
        data = {
            **self.data,
            "is_staff": True,
            "is_superuser": True,
            "is_active": False,
        }

        response = self.signup(data)
        user = User.objects.first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_active, True)


class SigninTests(AuthAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {
            "email": fake.email(),
            "password": fake.password(),
        }
        cls.user = UserFactory(**cls.data)

    def test_signin(self):
        response = self.signin(self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signin_last_login(self):
        response = self.signin(self.data)
        prev_login = response.data.get("user").get("last_login")

        response = self.signin(self.data)
        last_login = response.data.get("user").get("last_login")

        self.assertGreater(last_login, prev_login)

    def test_signin_email_wrong(self):
        data = {**self.data, "email": fake.email()}
        response = self.signin(data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_signin_password_wrong(self):
        data = {**self.data, "password": fake.password()}
        response = self.signin(data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_signin_data_insufficient(self):
        data = self.data.copy()
        data.pop("password")
        response = self.signin(data)

        self.assertContains(response, "password", None, status.HTTP_400_BAD_REQUEST)

        data = self.data.copy()
        data["email"] = ""
        response = self.signin(data)

        self.assertContains(response, "email", None, status.HTTP_400_BAD_REQUEST)


class SignoutTests(AuthAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.token = jwt_token_of(cls.user)
        cls.data = {"refresh": cls.token.get("refresh")}

    def setUp(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.get('access')}")

    def test_signout(self):
        response = self.signout(self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.signout(self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_signout_refresh_token_wrong(self):
        data = self.data.copy()
        data.update({"refresh": fake.password()})
        response = self.signout(data)

        self.assertContains(response, "refresh", None, status.HTTP_400_BAD_REQUEST)

    def test_signout_refresh_token_missing(self):
        data = self.data.copy()
        data["refresh"] = ""
        response = self.signout(data)

        self.assertContains(response, "refresh", None, status.HTTP_400_BAD_REQUEST)

    def test_signout_access_token_missing(self):
        self.client.credentials()
        response = self.signout(self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
