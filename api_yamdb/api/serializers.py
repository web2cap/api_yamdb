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
