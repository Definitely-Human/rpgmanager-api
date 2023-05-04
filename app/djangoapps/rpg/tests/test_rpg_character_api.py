"""Tests for rpg character API."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from djangoapps.rpg.models import Character
from djangoapps.rpg import serializers


CHARACTER_URL = reverse("rpg:character-list")


def detail_url(char_id):
    """Return character url given Id."""
    return reverse("rpg:character-detail", args=[char_id])


def create_user(email="user@example.com", password="testpass123", username="user"):
    """Create and return user."""
    return get_user_model().objects.create_user(
        email=email, password=password, username=username
    )


class PublicRPGCharacterAPITest(TestCase):
    """Unauthenticated API tests for RPG character."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required to get characters."""
        res = self.client.get(CHARACTER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRPGCharacterAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_character(self):
        """Test retrieving list of characters."""
        Character.objects.create(user=self.user, name="Bob")

        res = self.client.get(CHARACTER_URL)

        characters = Character.objects.all().order_by("name")
        serializer = serializers.CharacterSerializer(characters, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_character(self):
        """Test updating a character."""
        character = Character.objects.create(
            user=self.user,
            name="Bob",
        )

        payload = {"name": "Ralf"}
        url = detail_url(character.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        character.refresh_from_db()
        self.assertEqual(character.name, payload["name"])
