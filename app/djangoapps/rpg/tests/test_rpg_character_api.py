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


def create_user(
    email="user@example.com",
    password="testpass123",
    username="user",
):
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
        secondUser = create_user(email="user2@example.com", username="user2")
        Character.objects.create(user=secondUser, name="Rob")
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

    def test_delete_character(self):
        """Test deleting a character."""
        character = Character.objects.create(user=self.user, name="Bob")

        url = detail_url(character.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        character = Character.objects.filter(user=self.user)
        self.assertFalse(character.exists())

    def test_create_character(self):
        """Test creating a character."""
        payload = {
            "name": "Bob",
            "character_xp": 5,
        }

        res = self.client.post(CHARACTER_URL, payload)
        character = Character.objects.get(id=res.data["id"])
        for k, v in payload.items():
            self.assertEqual(getattr(character, k), v)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.user, character.user)

    def test_create_second_character_fails(self):
        """Test user can't create second character."""
        Character.objects.create(user=self.user, name="Bob")

        payload = {
            "name": "Rob",
            "character_xp": 5,
        }

        res = self.client.post(CHARACTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_other_user_character_fails(self):
        Character.objects.create(user=self.user, name="Bob")
        secondUser = create_user(email="user2@example.com", username="user2")
        originalName = "Rob"
        secondChar = Character.objects.create(
            user=secondUser, name=originalName
        )

        payload = {
            "name": "Bob2",
            "character_xp": 5,
        }
        res = self.client.patch(detail_url(secondChar.id), payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        secondChar.refresh_from_db()
        self.assertEqual(secondChar.name, originalName)
