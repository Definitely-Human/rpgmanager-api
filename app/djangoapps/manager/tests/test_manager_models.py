"""Test for manager app models."""

from django.test import TestCase
from djangoapps.manager import models
from djangoapps.rpg.models import Character
from django.contrib.auth import get_user_model


class ManagerTaskTests(TestCase):
    """Tests for manager task model."""

    def test_create_new_task(self):
        """Test creating new task."""
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="testpass",
            username="testuser",
        )
        character = Character.objects.create(user=user, name="Bob")
        task = models.Task.objects.create(
            character=character, title="Eat", content="Eat a lot"
        )
        self.assertEqual(str(task), task.title)
