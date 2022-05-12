from django.shortcuts import get_object_or_404
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    "Сериалайзер для Users."

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "bio",
        )
        lookup_field = "username"


class UserSignupSerializer(serializers.ModelSerializer):
    "Сериалайзер для самостоятельной регистрации пользователей."

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Такой username недопустим.")
        return value

    class Meta:
        model = User
        fields = ("username", "email")


class UserConfirmCodeSerializer(serializers.Serializer):
    "Сериалайзер для проверки username с кодом подтверждения."

    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=64, required=True)

    def validate(self, data):
        """Проверка соответстствия кода логину."""

        user = get_object_or_404(User, username=data["username"])
        if user.confirmation_code == data["confirmation_code"]:
            return data
        raise serializers.ValidationError("Неправильный username или код.")
