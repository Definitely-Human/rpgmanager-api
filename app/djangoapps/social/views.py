"""
Views for the social APIs.
"""
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from djangoapps.social.models import Profile
from djangoapps.social import serializers


class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """View for manage profile APIs."""

    serializer_class = serializers.ProfileSerializer
    queryset = Profile.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == "retrieve":
            return self.queryset
        return self.queryset.filter(user=self.request.user)
