from django.conf import settings
from django.db import models
from django.urls import reverse

from team_finder.constants import ProjectState, STATUS_MAX_LENGTH, TITLE_MAX_LENGTH


class Project(models.Model):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects',
        verbose_name='Автор'
    )
    title = models.CharField(max_length=TITLE_MAX_LENGTH, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    status = models.CharField(
        max_length=STATUS_MAX_LENGTH,
        choices=ProjectState,
        default=ProjectState.OPEN,
        verbose_name='Статус'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='joined_projects',
        blank=True,
        verbose_name='Участники'
    )
    favorited_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorite_projects',
        blank=True,
        verbose_name='Добавили в избранное'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:project-detail', kwargs={'pk': self.pk})

    @property
    def owner(self):
        return self.author

    @property
    def name(self):
        return self.title

    @property
    def created_at(self):
        return self.pub_date

    @property
    def github_url(self):
        return ''
