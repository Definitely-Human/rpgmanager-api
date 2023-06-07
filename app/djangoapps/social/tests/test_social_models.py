"""
Tests for social models.
"""

from django.test import TestCase
from djangoapps.social import models
from django.contrib.auth import get_user_model
from unittest.mock import patch


class SocialModelTests(TestCase):
    """Test social models."""

    def test_profile_created_for_new_user(self):
        """Test that profile is always create for a new user."""
        email = "test@example.com"
        username = "test"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email, username=username, password=password
        )
        self.assertIsInstance(user.profile, models.Profile)

        # TODO add tests to ensure user can't have 2 profiles

    @patch("djangoapps.social.models.uuid.uuid4")
    def test_profile_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.profile_image_file_path(None, "example.jpg")

        self.assertEqual(file_path, f"uploads/profile/{uuid}.jpg")
