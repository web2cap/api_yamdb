from django.contrib.auth.models import AbstractUser
from django.core.management.utils import get_random_secret_key
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("user", "Пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Администратор"),
    )

    def get_secret_key():
        return get_random_secret_key()

    email = models.EmailField(
        "Электронная почта",
        blank=False,
        null=False,
        max_length=254,
    )
    role = models.CharField(
        "Роль",
        choices=ROLE_CHOICES,
        default="user",
        blank=False,
        max_length=32,
    )
    bio = models.TextField(
        "Биография",
        blank=True,
        null=True,
        default=None,
    )
    confirmation_code = models.CharField(
        "Код подтверждения", max_length=64, default=get_secret_key()
    )

    def __str__(self):
        return self.username
