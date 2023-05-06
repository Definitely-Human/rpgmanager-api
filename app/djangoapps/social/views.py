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


class ProfileViewSet(
    viewsets.ViewSet
):  # TODO Change this to GenericViewSet and mixins
    """View for manage profile APIs."""

    queryset = Profile.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get profile for the current user.
        Does not return list despite its name.
        """
        profile = get_object_or_404(self.queryset, pk=request.user.profile.id)
        serializer_class = serializers.ProfileSerializer(profile)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        """Get profile for OTHER user."""
        profile = get_object_or_404(self.queryset, pk=pk)
        serializer_class = serializers.ProfileSerializer(profile)
        return Response(serializer_class.data)

    def partial_update(self, request, pk=None):
        """Update user profile."""
        if request.user.id != get_object_or_404(self.queryset, pk=pk).user.id:
            return Response(status=403)
        profile = Profile.objects.get(pk=pk)
        serializer = serializers.ProfileSerializer(
            profile, data=request.data, partial=True
        )  # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(status=201, data=serializer.data)
        return Response(status=400, data="wrong parameters")
