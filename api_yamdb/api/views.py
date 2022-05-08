from django.shortcuts import get_object_or_404
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User

from .permissions import MethodPostOnly
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        print(self.request.user)
        return super().get_queryset()


class AuthViewSet(viewsets.ModelViewSet):
    permission_classes = (MethodPostOnly,)
    # serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        return Response({"bug": "vulnerability"})

    @action(detail=False, methods=["post"])
    def token(self, request):
        if "username" not in request.data:
            raise exceptions.AuthenticationFailed("No username in request")
        if "confirmation_code" not in request.data:
            raise exceptions.AuthenticationFailed(
                "No confirmation_code in request"
            )
        user = get_object_or_404(
            User,
            username=request.data["username"],
        )
        if user.confirmation_code != request.data["confirmation_code"]:
            raise exceptions.AuthenticationFailed("Wrong confirmation_code")
        access_token = str(AccessToken.for_user(user))
        return Response({"access": access_token})
