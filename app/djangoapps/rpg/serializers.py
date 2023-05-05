"""Serializers for RPG app."""

from rest_framework import serializers

from djangoapps.rpg.models import Character


class CharacterSerializer(serializers.ModelSerializer):
    """Serializer for characters."""

    class Meta:
        model = Character
        fields = ["id", "name", "character_xp", "coins"]
        read_only_fields = ["id"]

    def validate(self, data):
        if (
            Character.objects.filter(
                user=self.context["request"].user
            ).exists()
            and self.context["request"].method == "POST"
        ):
            raise serializers.ValidationError("User already has character.")
        return data
