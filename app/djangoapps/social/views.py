"""
Views for the social APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from djangoapps.social.models import Profile
from djangoapps.social import serializers


class ProfileViewSet(viewsets.ViewSet):
    """View for manage profile APIs."""

    queryset = Profile.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get profile for the current user."""
        profile = get_object_or_404(self.queryset, pk=request.user.id)
        serializer_class = serializers.ProfileSerializer(profile)
        return Response(serializer_class.data)
