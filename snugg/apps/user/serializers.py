from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from snugg.tokens import AccessToken, RefreshToken, jwt_token_of

from .models import User


class SignupService(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password", "birth_date")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
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
        update_last_login(None, user)
        user_data = UserSerializer(user).data

        return user_data, jwt_token_of(user)


class SignoutService(serializers.Serializer):
    refresh = serializers.CharField()

    def validate_refresh(self, value):
        try:
            RefreshToken(value)
        except TokenError:
            raise serializers.ValidationError("유효하지 않은 토큰입니다.")

        return value

    @transaction.atomic
    def execute(self):
        refresh_token = RefreshToken(self.validated_data.get("refresh"))
        refresh_token.blacklist()

        request = self.context.get("request")
        access_token = AccessToken(request.META.get("HTTP_AUTHORIZATION").split()[1])
        access_token.blacklist()

        return True


class RefreshService(SignoutService, TokenRefreshSerializer):
    token_class = RefreshToken

    def execute(self):
        return {"access": self.validated_data.get("access")}


class UserSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(
        format="%Y-%m-%d", input_formats=["%Y-%m-%d", "iso-8601"], required=False
    )

    class Meta:
        model = User
        fields = (
            "pk",
            "email",
            "username",
            "birth_date",
            "self_introduction",
            "created_at",
            "last_login",
        )
        read_only_fields = ("created_at", "last_login")

    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("이미 사용중인 이메일입니다.")
        self.context["email"] = value
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("이미 사용중인 아이디입니다.")
        self.context["username"] = value
        return value

    def validate_birth_date(self, value):
        if value > datetime.now().date():
            raise serializers.ValidationError("생년월일을 확인해주세요.")
        self.context["birth_date"] = value
        return value

    def validate_self_introduction(self, value):
        if len(value) > 100:
            raise serializers.ValidationError("자기소개는 100자 이내로 작성해주세요.")
        self.context["self_introduction"] = value
        return value

    def update(self):
        user = self.context["request"].user
        user.email = self.context.get("email", user.email)
        user.username = self.context.get("username", user.username)
        user.birth_date = self.context.get("birth_date", user.birth_date)
        user.self_introduction = self.context.get(
            "self_introduction", user.self_introduction
        )
        user.save()

        return user


class PasswordService(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context.get("request").user
        if not user.check_password(value):
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")

        return value

    def validate_new_password(self, value):
        # 패스워드 유효성 검사는 프론트엔드에서 처리하도록 한다.

        return value

    def execute(self):
        user = self.context.get("request").user
        user.set_password(self.validated_data.get("new_password"))
        user.save()

        return True


class UserPublicSerializer(serializers.ModelSerializer):
    """
    Similar to UserSerializer, but do not expose sensitive informations such as email.
    """

    class Meta:
        model = User
        fields = ("pk", "username", "created_at", "last_login")
