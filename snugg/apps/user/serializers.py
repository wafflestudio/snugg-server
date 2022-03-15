from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from snugg.tokens import AccessToken, RefreshToken, jwt_token_of

from .models import User


class SignupService(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password", "birth_date")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user_data = UserSerializer(user).data

        return user_data, jwt_token_of(user)


class SigninService(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)

        if user is None:
            raise AuthenticationFailed("이메일 또는 비밀번호를 확인하세요.")
        self.context["user"] = user

        return data

    def execute(self):
        user = self.context.get("user")
        user_data = UserSerializer(user).data

        return user_data, jwt_token_of(user)


class SignoutService(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate_refresh_token(self, value):
        try:
            RefreshToken(value)
        except TokenError:
            raise serializers.ValidationError("유효하지 않은 토큰입니다.")

        return value

    @transaction.atomic
    def execute(self):
        refresh_token = RefreshToken(self.validated_data.get("refresh_token"))
        refresh_token.blacklist()

        request = self.context.get("request")
        access_token = AccessToken(request.META.get("HTTP_AUTHORIZATION").split()[1])
        access_token.blacklist()

        return True


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "email", "username", "birth_date")
