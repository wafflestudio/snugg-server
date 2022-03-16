import factory
from django.test import TestCase
from factory.django import DjangoModelFactory
from faker import Faker
from rest_framework import status

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


class SignUpTests(TestCase):
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
        response = self.client.post("/auth/signup/", data=self.data)
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
        data = self.data.copy()
        data.update({"username": "jason"})
        response = self.client.post("/auth/signup/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)

    def test_signup_data_insufficient(self):
        data = self.data.copy()
        data.pop("email")
        response = self.client.post("/auth/signup/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = self.data.copy()
        data["password"] = ""
        response = self.client.post("/auth/signup/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_permissions(self):
        data = self.data.copy()
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
        cls.data = {
            "email": fake.email(),
            "password": fake.password(),
        }
        cls.user = UserFactory(**cls.data)

    def test_signin(self):
        response = self.client.post("/auth/signin/", data=self.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signin_last_login(self):
        response = self.client.post("/auth/signin/", data=self.data)
        prev_login = response.data.get("user").get("last_login")

        response = self.client.post("/auth/signin/", data=self.data)
        last_login = response.data.get("user").get("last_login")

        self.assertGreater(last_login, prev_login)

    def test_signin_email_wrong(self):
        data = self.data.copy()
        data.update({"email": data.get("email") + "a"})
        response = self.client.post("/auth/signin/", data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_signin_password_wrong(self):
        data = self.data.copy()
        data.update({"password": data.get("password") + "a"})
        response = self.client.post("/auth/signin/", data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_signin_data_insufficient(self):
        data = self.data.copy()
        data.pop("password")
        response = self.client.post("/auth/signin/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = self.data.copy()
        data["email"] = ""
        response = self.client.post("/auth/signin/", data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SignoutTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def setUp(self):
        token = jwt_token_of(self.user)
        self.data = {"refresh_token": token.get("refresh")}
        self.header = {"HTTP_AUTHORIZATION": f"Bearer {token.get('access')}"}

    def test_signout(self):
        response = self.client.post("/auth/signout/", data=self.data, **self.header)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post("/auth/signout/", data=self.data, **self.header)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_signout_refresh_token_wrong(self):
        data = self.data.copy()
        data.update({"refresh_token": fake.password()})
        response = self.client.post("/auth/signout/", data=data, **self.header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signout_refresh_token_missing(self):
        data = self.data.copy()
        data["refresh_token"] = ""
        response = self.client.post("/auth/signout/", data=data, **self.header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signout_access_token_missing(self):
        response = self.client.post("/auth/signout/", data=self.data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
