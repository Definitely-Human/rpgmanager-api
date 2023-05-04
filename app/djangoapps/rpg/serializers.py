"""Serializers for RPG app."""

from rest_framework import serializers

from djangoapps.rpg.models import Character


class CharacterSerializer(serializers.ModelSerializer):
    """Serializer for characters."""

    class Meta:
        model = Character
        fields = ["id", "name", "character_xp", "coins"]
        read_only_fields = ["id"]
