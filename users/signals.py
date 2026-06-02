"""Signal handlers for the users app."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from users.utils import _build_avatar


@receiver(post_save, sender=User)
def _on_user_created(sender, instance, created, **kwargs):
    """Set an initial avatar for newly created users."""
    if created and not instance.avatar:
        letter = (instance.first_name or instance.email[0] if instance.email else "?").upper()
        avatar_file = _build_avatar(letter)
        instance.avatar.save(f"avatar_{instance.pk}.png", avatar_file, save=True)
