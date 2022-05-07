from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("user", "Пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Администратор"),
    )
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

    def __str__(self):
        return self.username
