from datetime import datetime

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from snugg.tokens import RefreshToken

from .models import User


def jwt_token_of(user):
    refresh = RefreshToken.for_user(user)
    jwt_token = {"refresh": str(refresh), "access": str(refresh.access_token)}
    return jwt_token


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
            "password": {"required": True, "write_only": True},
            "birth_date": {"required": True},
        }

    def validate(self, data):
        email = data.get("email", None)
        username = data.get("username", None)
        password = data.get("password", None)
        birth_date = data.get("birth_date", None)

        if User.objects.filter(email=email).exists():
            raise ValidationError("이미 존재하는 이메일입니다.")

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user, jwt_token_of(user)


class UserSignInSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)

        if user is None:
            raise AuthenticationFailed("아이디 또는 비밀번호를 확인하세요.")

        return {"email": user.email, "token": jwt_token_of(user)}

    def create(self, data):
        return data
