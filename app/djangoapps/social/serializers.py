"""
Serializers for social app API.
"""
from rest_framework import serializers

from djangoapps.social.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for profiles."""

    class Meta:
        model = Profile
        fields = [
            "id",
            "is_online",
            "first_name",
            "last_name",
            "about_me",
            "image",
        ]
        read_only_fields = ["id", "is_online", "image"]


class ProfileImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading profile images."""

    class Meta:
        model = Profile
        fields = ["id", "image"]
        read_only_fields = ["id"]
        extra_kwargs = {"image": {"required": "True"}}
