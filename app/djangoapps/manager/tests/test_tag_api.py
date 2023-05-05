"""
Tests for manager tag APIs.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from djangoapps.manager.models import Tag
from djangoapps.manager.serializers import TagSerializer


TAGS_URL = reverse("manager:tag-list")


def create_user(
    email="user@example.com",
    password="testpass123",
    username="user",
):
    """Create and return user."""
    return get_user_model().objects.create_user(
        email=email, password=password, username=username
    )


def create_tag(user, name="Eating", description="About eating."):
    return Tag.objects.create(user=user, name=name, description=description)


class PublicTagsAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required to get tags."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_tags_list(self):
        """Test getting a list of tags."""
        Tag.objects.create(self.user)
        Tag.objects.create(
            self.user, name="Training", description="About training."
        )

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by("name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test list of tags limited to authenticated user."""
        user2 = create_user(email="user2@example.com", username="user2")
        create_tag(user2)
        tag = create_tag(self.user, name="Training")

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)
        self.assertEqual(res.data[0]["id"], tag.id)
