"""Tests for models in RPG app."""

from django.test import TestCase
from djangoapps.rpg import models
from django.contrib.auth import get_user_model


class RPGModelTests(TestCase):
    """Tests for RPG models."""

    def test_create_new_character():
        """Test creating new character."""
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass",
            username="testuser",
        )
        character = models.Character.objects.create(user=user, name="Bob")

        self.assertEqual(str(character), character.name)
