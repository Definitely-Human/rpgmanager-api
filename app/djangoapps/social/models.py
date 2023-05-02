"""
Models for social app.
"""

from django.db import models
from django.conf import settings


class Profile(models.Model):
    """Profile model."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    is_online = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    about_me = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

from django.dispatch import receiver
from django.db.models.signals import post_save

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_created_add_profile(sender, instance, created, *args, **kwargs):
    """
    Once a new User instance was saved:
    Check User instance, if this is new instance (created is True)
    then create a Profile for this user.
    """
    if not created:
        return
    instance.profile = Profile.objects.create(user=instance,first_name = instance.username)
