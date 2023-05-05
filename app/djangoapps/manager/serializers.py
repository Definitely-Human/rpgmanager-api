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


class TaskDetailSerializer(TaskSerializer):
    """Serializer for task detail view."""

    class Meta(TaskSerializer.Meta):
        fields = TaskSerializer.Meta.fields + [
            "content",
            "created_at",
            "completion_time",
        ]
        read_only_fields = TaskSerializer.Meta.read_only_fields + [
            "created_at",
            "completion_time",
        ]
