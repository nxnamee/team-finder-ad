from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os


def build_avatar(instance, filename):
    ext = filename.split('.')[-1]
    path = f'avatars/{instance.username}_avatar.{ext}'
    return path
