"""
Views for the RPG app APIs.
"""

from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from djangoapps.rpg.models import Character
from djangoapps.rpg import serializers


class CharacterViewSet(viewsets.ModelViewSet):
    """Views to manage Character API."""

    serializer_class = serializers.CharacterSerializer
    queryset = Character.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter character to make sure user can only edit their character."""
        if self.action == "list" or self.action == "retrieve":
            return self.queryset.order_by("name")
        return self.queryset.filter(user=self.request.user)
