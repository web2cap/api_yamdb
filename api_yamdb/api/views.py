from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

from .permissions import (
    MeOrAdmin,
    PostOnlyNoCreate,
)
from .serializers import UserSerializer


class AuthViewSet(viewsets.ModelViewSet):
    permission_classes = (PostOnlyNoCreate,)

    @action(detail=False, methods=["post"])
    def token(self, request):
        if "username" not in request.data:
            return Response(
                {"detail": "No username in request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if "confirmation_code" not in request.data:
            return Response(
                {"detail": "No confirmation_code in request"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_object_or_404(
            User,
            username=request.data["username"],
        )
        if user.confirmation_code != request.data["confirmation_code"]:
            return Response(
                {"detail": "Wrong confirmation_code"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        access_token = str(AccessToken.for_user(user))
        return Response({"access": access_token})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (MeOrAdmin,)
    lookup_field = "username"

    def retrieve(self, request, username=None):
        """Получение экземпляра пользователя по username.
        При запросе на /me/ возвращает авторизованного пользователя."""

        queryset = User.objects.all()
        if username == "me":
            username = request.user.username
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def partial_update(self, request, username=None):
        """Обновление экземпляра пользователя по username.
        Не позволяет установить непредусмотренную роль.
        Если пользователь не админ, не позволяет сменить роль."""

        data = request.data.copy()
        if "role" in data:
            if data["role"] not in ("user", "admin", "moderator"):
                return Response(
                    {"detail": "Wrong role"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not request.user.is_admin:
                data.pop("role")
        serializer = UserSerializer(request.user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    def destroy(self, request, username=None):
        """Удаление пользователя.
        Не позволяет удалить самого себя при запросе на /me/."""

        if username == "me":
            return Response(
                {"detail": "You can't delete yourself"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
