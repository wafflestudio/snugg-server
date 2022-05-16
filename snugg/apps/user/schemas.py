from drf_spectacular.utils import (OpenApiResponse, extend_schema,
                                   extend_schema_view)
from rest_framework import serializers

from .examples import TestUser
from .serializers import UserSerializer


class Token(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()


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
)
