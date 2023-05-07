"""Serializers for manager app."""

from rest_framework import serializers

from djangoapps.manager.models import (
    Task,
    Tag,
    Category,
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

    def _get_or_create_tags(self, tags, task):
        """Handle getting or creating tags as needed."""
        auth_user = self.context["request"].user

        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            task.tags.add(tag_obj)

    def create(self, validated_data):
        """Create new task."""
        tags = validated_data.pop("tags", [])
        task = Task.objects.create(**validated_data)
        self._get_or_create_tags(tags, task)

        return task

    def update(self, instance, validated_data):
        """Update task."""
        tags = validated_data.pop("tags", None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category."""

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "subcategory_of",
        ]
        read_only_fields = [
            "id",
        ]
