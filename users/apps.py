"""App config for users."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Users application settings."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
    verbose_name = "Пользователи"

    def ready(self):
        """Register signal handlers."""
        import users.signals
