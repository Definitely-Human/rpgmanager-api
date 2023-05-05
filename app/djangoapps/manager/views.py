"""
Views for the manager APIs.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from djangoapps.manager.models import Task
from djangoapps.manager import serializers


class TaskViewSet(viewsets.ModelViewSet):
    """View for managing task APIs."""

    serializer_class = serializers.TaskSerializer
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve tasks for authenticated user."""
        return self.queryset.filter(
            character=self.request.user.character
        ).order_by("-id")
