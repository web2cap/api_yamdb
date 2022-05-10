from django.shortcuts import get_object_or_404
from requests import request
from rest_framework import status, viewsets
from rest_framework.decorators import action

# from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import PermissionDenied
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

from .permissions import (
    # IsRoleAdmin,
    MeGetPatchOnlyOrAdmin,
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
    permission_classes = (MeGetPatchOnlyOrAdmin,)
    lookup_field = "username"

    """
    def get_permissions(self):
        # print(self.action)
        # print("SELF")
        # print(self)
        print(self.__dir__())

        if self.action == "retrieve":
            permission_classes = (OwnerUserOrAdminGetPatchOnly,)
        else:
            permission_classes = (IsRoleAdmin,)
        return [permission() for permission in permission_classes]
    """

    def retrieve(self, request, username=None):
        queryset = User.objects.all()
        if username == "me":
            username = request.user.username
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def partial_update(self, request, username=None):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True
        )
        print(serializer.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

    """
    @action(detail=False, methods=["get", "patch"])
    def me(self, request):
        print("##### HERE")
        print(request.user.pk)
        current_user = User.objects.filter(pk=request.user.pk)
        serializer = self.get_serializer(current_user, many=False)
        return Response(serializer.data)
    """


"""
class UserMeViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (OwnerUserGetPatchOnly,)
    pagination_class = None
    # queryset = User.objects.filter(pk=request.user)

    def get_queryset(self):
        # print(self.request.user)
        return User.objects.filter(pk=self.request.user.pk)

"""
