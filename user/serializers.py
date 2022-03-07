from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from snugg.tokens import RefreshToken
from .models import User
from datetime import datetime

def jwt_token_of(user):
    refresh = RefreshToken.for_user(user)
    jwt_token = {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
    return jwt_token


class UserCreateSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    birth_date = serializers.CharField(required=True)

    is_staff = serializers.BooleanField(default=False)
    is_superuser = serializers.BooleanField(default=False)
    is_active = serializers.BooleanField(default=True)
    is_admin = serializers.BooleanField(default=False)

    def validate(self, data):
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)
        birth_date = data.get('birth_date', None)
        data['birth_date'] = datetime.strptime(birth_date, '%Y-%m-%d')

        if User.objects.filter(email=email).exists():
            raise ValidationError('이미 존재하는 이메일입니다.')

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user, jwt_token_of(user)
