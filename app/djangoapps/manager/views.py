"""
Views for the manager APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from djangoapps.manager.models import (
    Task,
    Tag,
)
from djangoapps.manager import serializers


class TaskViewSet(viewsets.ModelViewSet):
    """View for managing task APIs."""

    serializer_class = serializers.TaskDetailSerializer
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve tasks for authenticated user."""
        return self.queryset.filter(
            character=self.request.user.character
        ).order_by("-id")

    def get_serializer_class(self):
        """Return serializer class for request."""
        if self.action == "list":
            return serializers.TaskSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create new task."""
        serializer.save(character=self.request.user.character)


class TagViewSet(viewsets.ModelViewSet):
    """View for managing tag APIs."""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve tags for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("name")

    def perform_create(self, serializer):
        """Create new tag."""
        serializer.save(user=self.request.user)
