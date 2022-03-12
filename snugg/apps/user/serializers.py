from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from snugg.tokens import RefreshToken

from .models import User


def jwt_token_of(user):
    refresh = RefreshToken.for_user(user)
    jwt_token = {"refresh": str(refresh), "access": str(refresh.access_token)}
    return jwt_token


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password", "birth_date")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user_data = UserSerializer(user).data

        return user_data, jwt_token_of(user)


class UserSignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)

        if user is None:
            raise AuthenticationFailed("이메일 또는 비밀번호를 확인하세요.")

        return {"user": user}

    def create(self, validated_data):
        user = validated_data.get("user")
        user_data = UserSerializer(user).data

        return user_data, jwt_token_of(user)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "email", "username", "birth_date")
