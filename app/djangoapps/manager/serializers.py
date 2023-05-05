"""Serializers for manager app."""

from rest_framework import serializers

from djangoapps.manager.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for listing tasks."""

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "is_complete",
            "is_favorite",
            "due_to",
            "updated_at",
        ]
        read_only_fields = ["id", "updated_at"]
