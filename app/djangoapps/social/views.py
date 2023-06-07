"""
Views for the social APIs.
"""
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
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

    queryset = Profile.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Return serializer for the request."""
        if self.action == "upload_image":
            return serializers.ProfileImageSerializer
        return serializers.ProfileSerializer

    def get_queryset(self):
        if self.action == "retrieve":
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Custom endpoint to upload image to the profile."""
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
