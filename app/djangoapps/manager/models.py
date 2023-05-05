"""Models for manager app."""

from django.db import models
from django.utils import timezone


class Task(models.Model):
    """Task model."""

    character = models.ForeignKey("rpg.Character", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_index=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_to = models.DateTimeField(null=True)
    completion_time = models.DateTimeField(null=True)
    is_complete = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ["is_complete", "created_at"]
