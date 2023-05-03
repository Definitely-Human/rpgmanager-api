"""
Tests for social APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from djangoapps.social.models import Profile
from djangoapps.social.serializers import ProfileSerializer


OWN_PROFILE_URL = reverse("social:profile")


class PublicProfileAPITests(TestsCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_get_own_profile_auth_required(self):
        """Test auth is required to call self profile API."""
        res = self.client.get(OWN_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProfileAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass123",
            username="testuser",
        )
        user.profile.first_name = "Testfirstname"
        user.profile.last_name = "Testlastname"
        user.profile.save()
        self.client.force_authenticate(self.user)

    def test_retrieve_own_profile(self):
        """Test retrieving own profile when authenticated."""
        res = self.client.get(OWN_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
