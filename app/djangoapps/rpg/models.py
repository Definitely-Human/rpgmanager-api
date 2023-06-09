"""Models for RPG app."""

from django.db import models
from django.conf import settings


class Character(models.Model):
    """Model representing the character of the user."""

    name = models.CharField(max_length=100)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    character_xp = models.PositiveIntegerField(
        default=0,
    )
    coins = models.IntegerField(default=0)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return self.name
