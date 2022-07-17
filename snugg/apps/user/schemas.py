from lib2to3.pgen2.token import OP
from tkinter.filedialog import Open

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework import serializers

from .examples import TestUser
from .serializers import UserSerializer


class RefreshToken(serializers.Serializer):
    refresh = serializers.CharField()


class AccessToekn(serializers.Serializer):
    access = serializers.CharField()


class Token(AccessToekn, RefreshToken):
    pass


class UserToken(serializers.Serializer):

    user = UserSerializer()
    token = Token()


class Success(serializers.Serializer):
    success = serializers.BooleanField()


auth_viewset_schema = extend_schema_view(
    signup=extend_schema(
        summary="Signup",
        description="Create new user.",
        responses={
            201: OpenApiResponse(
                response=UserToken, examples=[TestUser.signup_example]
            ),
            400: OpenApiResponse(description="Invalid or insufficient data."),
        },
    ),
    signin=extend_schema(
        summary="Signin",
        description="Get refresh token and access token.",
        responses={
            200: OpenApiResponse(
                response=UserToken, examples=[TestUser.signin_example]
            ),
            400: OpenApiResponse(description="Incorrect or insufficient data."),
        },
    ),
    signout=extend_schema(
        summary="Signout",
        description="Expire refresh token and access token.",
        responses={
            200: OpenApiResponse(response=Success),
            400: OpenApiResponse(description="Incorrect or missing refresh token."),
            401: OpenApiResponse(
                description="Missing authorization header, or access token expired."
            ),
        },
    ),
    refresh=extend_schema(
        summary="Refresh Token",
        description="Renew refresh token and get new accesss token",
        responses={
            200: OpenApiResponse(response=RefreshToken),
            400: OpenApiResponse(description="Incorrect or missing refresh token."),
        },
    ),
    password=extend_schema(
        summary="Password",
        description="Change password for user.",
        responses={
            200: OpenApiResponse(response=Success),
            400: OpenApiResponse(description="Incorrect password."),
        },
        parameters=[
            OpenApiParameter(
                name="old_password",
                location="body",
                type=OpenApiTypes.STR,
                description="기존 비밀번호를 입력해야 합니다.",
                required=True,
            ),
            OpenApiParameter(
                name="new_password",
                location="body",
                type=OpenApiTypes.STR,
                description="새 비밀번호를 입력해야 합니다.",
                required=True,
            ),
        ],
    ),
    profile=extend_schema(
        summary="Profile",
        description="See or update profile for user.",
        responses={
            200: OpenApiResponse(response=UserSerializer),
            400: OpenApiResponse(description="Incorrect or insufficient data."),
        },
    ),
)
