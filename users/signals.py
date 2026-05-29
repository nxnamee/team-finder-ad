from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def handle_new_user(sender, instance, created, **kw):
    if created:
        g, _ = Group.objects.get_or_create(name='members')
        instance.groups.add(g)
