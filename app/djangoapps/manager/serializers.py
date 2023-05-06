"""Serializers for manager app."""

from rest_framework import serializers

from djangoapps.manager.models import (
    Task,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for listing tasks."""

    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "is_complete",
            "is_favorite",
            "due_to",
            "updated_at",
            "tags",
        ]
        read_only_fields = ["id", "updated_at"]

    def create(self, validated_data):
        """Create new task."""
        tags = validated_data.pop("tags", [])
        task = Task.objects.create(**validated_data)
        auth_user = self.context["request"].user

        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            task.tags.add(tag_obj)

        return task


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
