"""
Models for social app.
"""

from django.db import models


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
