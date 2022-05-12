from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Title
from users.models import User

from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    ReadOnlyTitleSerializer,
    TitleSerializer,
    UserConfirmCodeSerializer,
    UserSerializer,
    UserSignupSerializer,
)
from .permissions import MeOrAdmin, PostOnlyNoCreate, RoleAdminrOrReadOnly


class AuthViewSet(viewsets.ModelViewSet):
    """Получение токена авторизации JWT в ответ на POST запрос, на адрес /token.
    Регистрация пользователей на эндпоинте /signup.
    POST на корневой эндпоитн и другие типы запросов запрешены пермищенном.
    """

    permission_classes = (PostOnlyNoCreate,)

    @action(detail=False, methods=["post"])
    def token(self, request):
        """Получение токена по username и confirmation_code."""

        serializer = UserConfirmCodeSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=serializer.data["username"]
            )
            access_token = str(AccessToken.for_user(user))
            return Response(
                {"access": access_token}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            if (
                "username" in serializer.data
                and User.objects.filter(
                    username=serializer.data["username"],
                    email=serializer.data["email"],
                ).exists()
            ):
                self.send_mail_code(serializer.data)
                return Response(
                    {"detail": "Письмо с кодом подтверждения отправленно"},
                    status=status.HTTP_200_OK,
                )
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


class CategoryViewSet(ListCreateDestroyViewSet):
    """API для работы с моделью категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (RoleAdminrOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(ListCreateDestroyViewSet):
    """API для работы с моделью жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (RoleAdminrOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """API для работы произведений."""

    queryset = (
        Title.objects.all().annotate(Avg("reviews__score")).order_by("name")
    )
    permission_classes = (RoleAdminrOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer
