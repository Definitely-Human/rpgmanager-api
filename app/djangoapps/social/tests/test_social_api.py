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


OWN_PROFILE_URL = reverse("social:profile-list")


def profile_by_id(profile_id):
    """Create and return URL for profile of other user."""
    return reverse("social:profile-detail", args=[profile_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicProfileAPITests(TestCase):
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
        self.user = create_user(
            email="user@example.com",
            password="testpass123",
            username="testuser",
        )
        self.user.profile.first_name = "Testfirstname"
        self.user.profile.last_name = "Testlastname"
        self.user.profile.about_me = "testAbout"
        self.user.profile.save()
        self.client.force_authenticate(self.user)

    def test_retrieve_own_profile(self):
        """Test retrieving own profile when authenticated."""
        res = self.client.get(OWN_PROFILE_URL)
        serializer = ProfileSerializer(self.user.profile)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0], serializer.data)

    def test_get_other_user_profile(self):
        """Test get other user profile."""
        otherUser = create_user(
            email="user2@example.com",
            password="testpass123",
            username="testuser2",
        )
        otherUser.profile.first_name = "SecondFirstName"
        otherUser.profile.last_name = "SecondLastName"
        otherUser.profile.save()

        url = profile_by_id(otherUser.profile.id)
        res = self.client.get(url)

        serializer = ProfileSerializer(otherUser.profile)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_own_profile_successful(self):
        """Test updating users own profile."""
        original_about = self.user.profile.about_me
        payload = {
            "first_name": "newFirstName",
            "last_name": "newLastName",
        }

        res = self.client.patch(profile_by_id(self.user.profile.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        profile = Profile.objects.get(id=res.data["id"])
        for k, v in payload.items():
            self.assertEqual(getattr(profile, k), v)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.about_me, original_about)

    def test_update_other_user_profile_fail(self):
        """Test updating other users profile fails."""
        otherUser = create_user(
            email="user2@example.com",
            password="testpass123",
            username="testuser2",
        )
        originalUserName = "SecondFirstName"
        otherUser.profile.first_name = originalUserName
        otherUser.profile.save()

        payload = {
            "first_name": "newFirstName",
        }

        res = self.client.patch(profile_by_id(otherUser.profile.id), payload)
        otherUser.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(otherUser.profile.first_name, originalUserName)
        self.assertEqual(otherUser.profile.user, otherUser)

    def test_deleting_own_profile_not_allowed(self):
        """Test not possible to delete own profile."""
        res = self.client.delete(OWN_PROFILE_URL)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_deleting_others_profile_not_allowed(self):
        """Test not possible to delete own profile."""
        otherUser = create_user(
            email="user2@example.com",
            password="testpass123",
            username="testuser2",
        )
        res = self.client.delete(profile_by_id(otherUser.profile.id))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_changing_user_not_possible(self):
        """Test that changing user for profile is not possible."""
        otherUser = create_user(
            email="user2@example.com",
            password="testpass123",
            username="testuser2",
        )
        profile = self.user.profile
        payload = {"user": otherUser.id}

        url = profile_by_id(self.user.profile.id)
        self.client.patch(url, payload)

        profile.refresh_from_db()
        self.assertEqual(self.user.profile, profile)
