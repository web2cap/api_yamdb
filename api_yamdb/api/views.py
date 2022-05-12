from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Title, User

from .filters import TitlesFilter
from .mixins import ListCreateDestroyViewSet
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    ReadOnlyTitleSerializer,
    TitleSerializer,
    UserSerializer
)
from .permissions import (
    MeOrAdmin,
    PostOnlyNoCreate,
    RoleAdminrOrReadOnly
)


class AuthViewSet(viewsets.ModelViewSet):
    """Получение токена авторизации JWT в ответ на POST запрос, на адрес /token.
    POST на корневой эндпоитн и другие типы запросов запрешены пермищенном."""

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
