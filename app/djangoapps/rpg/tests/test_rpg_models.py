"""Tests for models in RPG app."""

from django.test import TestCase
from djangoapps.rpg import models
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


class RPGModelTests(TestCase):
    """Tests for RPG models."""

    def test_create_new_character(self):
        """Test creating new character."""
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass",
            username="testuser",
        )
        character = models.Character.objects.create(user=user, name="Bob")

        self.assertEqual(str(character), character.name)

    def test_creating_character_fails_if_one_exists(self):
        """Test user can't create second character."""
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass",
            username="testuser",
        )
        character = models.Character.objects.create(user=user, name="Bob")

        self.assertRaises(
            IntegrityError, models.Character.objects.create, user=user, name="Tom"
        )
