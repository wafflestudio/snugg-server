from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from snugg.tokens import AccessToken, RefreshToken

from .serializers import UserCreateSerializer, UserSignInSerializer


class UserAccountViewSet(GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCreateSerializer

    @action(detail=False, methods=["POST"])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user, jwt_token = serializer.save()
        except IntegrityError:
            # 추후 커스텀 에러로 변경 예정
            raise IntegrityError()

        return Response(
            {"user": user.username, "token": jwt_token}, status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["POST"])
    def signin(self, request):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()

        return Response({"success": True, "token": token}, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def signout(self, request):
        refresh_token = RefreshToken(request.data.get("refresh"))
        access_token = AccessToken(request.META.get("HTTP_AUTHORIZATION").split()[1])
        refresh_token.blacklist()
        access_token.blacklist()
        return Response({"success": True})

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def deactivate(self, request):
        user = authenticate(
            email=request.user.email, password=request.data.get("password")
        )
        if user is not request.user:
            raise AuthenticationFailed("아이디 또는 비밀번호를 확인하세요.")
        self.signout(request)
        user.is_active = False
        user.save()
        return Response({"success": True})
