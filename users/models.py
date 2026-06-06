"""Custom User model with inline profile fields."""

from django.contrib.auth.models import AbstractUser
from django.db import models

from team_finder.constants import MAX_FIRST_NAME, MAX_LAST_NAME, PHONE_MAX_LENGTH


class User(AbstractUser):
    """Extended user with avatar, description, phone and github."""

    first_name = models.CharField("Имя", max_length=MAX_FIRST_NAME)
    last_name = models.CharField("Фамилия", max_length=MAX_LAST_NAME)
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    description = models.TextField(
        blank=True,
        verbose_name="О себе",
    )
    phone = models.CharField(
        max_length=PHONE_MAX_LENGTH,
        verbose_name="Телефон",
    )
    github = models.URLField(
        blank=True,
        verbose_name="GitHub",
    )

    class Meta:
        """User model meta."""

        ordering = ("-date_joined",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """Human-readable representation."""
        return self.email
