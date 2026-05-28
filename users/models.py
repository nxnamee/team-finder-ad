import io

from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image, ImageDraw, ImageFont

from team_finder.constants import (
    AVATAR_BACKGROUND_COLOR,
    AVATAR_SIZE,
    AVATAR_TEXT_COLOR,
    PHONE_MAX_LENGTH,
)


class User(AbstractUser):

    email = models.EmailField(unique=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True,
        verbose_name='Аватар'
    )
    description = models.TextField(
        blank=True,
        verbose_name='О себе'
    )
    phone = models.CharField(
        max_length=PHONE_MAX_LENGTH,
        blank=True,
        verbose_name='Телефон'
    )
    github = models.URLField(
        blank=True,
        verbose_name='GitHub'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def name(self):
        return self.first_name

    @property
    def surname(self):
        return self.last_name

    @property
    def about(self):
        return self.description

    @property
    def github_url(self):
        return self.github

    @property
    def owned_projects(self):
        return self.projects.all()


def _generate_initial_avatar(letter):
    img = Image.new('RGB', (AVATAR_SIZE, AVATAR_SIZE), AVATAR_BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (AVATAR_SIZE - text_width) // 2
    y = (AVATAR_SIZE - text_height) // 2 - 5
    draw.text((x, y), letter, fill=AVATAR_TEXT_COLOR, font=font)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue())


@receiver(post_save, sender=User)
def _create_user_avatar(sender, instance, created, **kwargs):
    if created and not instance.avatar:
        letter = (instance.first_name or instance.email[0] if instance.email else '?').upper()
        avatar_file = _generate_initial_avatar(letter)
        instance.avatar.save(f'avatar_{instance.pk}.png', avatar_file, save=True)
