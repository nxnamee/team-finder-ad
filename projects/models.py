from django.db import models
from django.conf import settings
from team_finder.constants import PROJECT_STATUSES, PARTICIPANT_ROLES

STATUS_OPTIONS = [(k, v) for k, v in PROJECT_STATUSES.items()]
ROLE_OPTIONS = [(k, v) for k, v in PARTICIPANT_ROLES.items()]


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects',
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Membership',
        related_name='participating_projects',
    )
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default='active')
    skills = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class Membership(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=ROLE_OPTIONS, default='developer')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'user')
        verbose_name_plural = 'memberships'


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')
