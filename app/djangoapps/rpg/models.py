"""Models for RPG app."""

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator


class Character(models.Model):
    """Model representing the character of the user."""

    name = models.CharField(max_length=100)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    character_xp = models.IntegerField(
        validators=[MinValueValidator],
        default=0,
    )
    coins = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name
