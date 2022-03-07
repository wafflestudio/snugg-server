from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User

class UserSignUpSerializer(serializers.Serializer):
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


        if User.objects.filter(email=email).exists():
            raise ValidationError('이미 존재하는 이메일입니다.')

        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)