"""
Serializers for social app API.
"""
from rest_framework import serializers

from djangoapps.social.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for profiles."""

    class Meta:
        model = Profile
        fields = ["id", "is_online", "first_name", "last_name", "about_me"]
        read_only_fields = ["id"]
