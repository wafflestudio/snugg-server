from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .schemas import auth_viewset_schema
from .serializers import (
    PasswordService,
    RefreshService,
    SigninService,
    SignoutService,
    SignupService,
    UserSerializer,
)


@auth_viewset_schema
class AuthViewSet(GenericViewSet):
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.AllowAny,),
        serializer_class=SignupService,
    )
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data, jwt_token = serializer.save()

        return Response(
            {"user": user_data, "token": jwt_token}, status=status.HTTP_201_CREATED
        )

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.AllowAny,),
        serializer_class=SigninService,
    )
    def signin(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data, jwt_token = serializer.execute()

        return Response({"user": user_data, "token": jwt_token})

    @action(
        detail=False,
        methods=["POST"],
        serializer_class=SignoutService,
    )
    def signout(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        success = serializer.execute()

        return Response({"success": bool(success)})

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=(permissions.AllowAny,),
        serializer_class=RefreshService,
    )
    def refresh(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        jwt_token = serializer.execute()

        return Response({"token": jwt_token})

    @action(
        detail=False,
        methods=["PUT"],
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=PasswordService,
    )
    def password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.execute()

        return Response({"notice": "비밀번호가 정상적으로 변경되었습니다. 새로운 비밀번호로 다시 로그인해주세요."})

    @action(
        detail=False,
        methods=["GET", "PUT"],
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=UserSerializer,
    )
    def profile(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = self.get_serializer(request.user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.update()
            return Response(serializer.data)
