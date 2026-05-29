from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    github = models.URLField(max_length=200, blank=True)
    linkedin = models.URLField(max_length=200, blank=True)
    website = models.URLField(max_length=200, blank=True)
    skills = models.JSONField(default=list, blank=True)
    role = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = 'users'
        ordering = ['-date_joined']
