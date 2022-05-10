from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend


from .permissions import PostOnlyNoCreate
from reviews.models import Title
from .filters import TitlesFilter

from .serializers import TitleSerializer, ReadOnlyTitleSerializer
from .permissions import PostOnlyNoCreate


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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")
    ).order_by("name")
    serializer_class = TitleSerializer
    permission_classes = (PostOnlyNoCreate,)
    http_method_names = ['get', 'pos', 'head', 'patch']
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        if self.action in ():
            return ReadOnlyTitleSerializer
        return TitleSerializer
