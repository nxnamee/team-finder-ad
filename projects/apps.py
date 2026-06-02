"""App config for projects."""

from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    """Projects application settings."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "projects"
    verbose_name = "Проекты"
