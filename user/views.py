from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import UserCreateSerializer


class UserSignUpViewSet(GenericViewSet):
    serializer_class = UserCreateSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()

        try:
            user, jwt_token = serializer.save()
        except IntegrityError:
            # 추후 커스텀 에러로 변경 예정
            raise IntegrityError()

        return Response(
            {"user": user.username, "token": jwt_token}, status=status.HTTP_201_CREATED
        )
