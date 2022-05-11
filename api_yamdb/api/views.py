import email
from django.core.mail import send_mail
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
from .serializers import UserSerializer, UserSignupSerializer


class AuthViewSet(viewsets.ModelViewSet):
    """Получение токена авторизации JWT в ответ на POST запрос, на адрес /token.
    Регистрация пользователей на эндпоинте /signup.
    POST на корневой эндпоитн и другие типы запросов запрешены пермищенном.
    """

    # serializer_class = UserSignupSerializer
    permission_classes = (PostOnlyNoCreate,)

    @action(detail=False, methods=["post"])
    def token(self, request):
        """Получение токена по username и confirmation_code."""

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

    @action(detail=False, methods=["post"])
    def signup(self, request):
        """Самостоятельная регистрация нового пользователя.
        Создает пользователя по запросу.
        Отправляет код подверждения пользователю на email.
        Отправляет код подверждения на email существующим пользователям."""

        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
        else:
            if "username" in serializer.data:
                user = User.objects.filter(
                    username=serializer.data["username"],
                    email=serializer.data["email"],
                )
                if user.exists():
                    self.send_mail_code(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        self.send_mail_code(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )

    def send_mail_code(self, data):
        """Функция отправки кода подтверждения."""

        user = get_object_or_404(User, username=data["username"])
        mail_text = "Добро пожаловать!\n"
        mail_text += f"Ваш код подтверждения YAMDB {user.confirmation_code}"
        mail_text += "\n\nКоманда YAMDB."
        result = send_mail(
            "YAMDB Ваш код подтверждения",
            mail_text,
            "noreplay@yamdb.team3",
            [data["email"]],
            fail_silently=False,
        )
        return result


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet API управления пользователями.
    Запросы к экземпляру осуществляются по username.
    При обращении на /me/ пользователь дополняет/получает свою запись."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (MeOrAdmin,)
    lookup_field = "username"

    def retrieve(self, request, username=None):
        """Получение экземпляра пользователя по username.
        При запросе на /me/ возвращает авторизованного пользователя."""

        if username == "me":
            username = request.user.username
        user = get_object_or_404(self.queryset, username=username)
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
