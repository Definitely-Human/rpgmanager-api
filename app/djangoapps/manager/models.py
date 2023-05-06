"""Models for manager app."""

from django.db import models
from django.conf import settings


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
    tags = models.ManyToManyField("Tag")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        ordering = ["is_complete", "created_at"]


class Tag(models.Model):
    """Tags model for filtering."""

    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # TODO Add unique together constraint to name and user
    description = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
    )
    name = models.CharField(max_length=50)
    subcategory_of = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]
