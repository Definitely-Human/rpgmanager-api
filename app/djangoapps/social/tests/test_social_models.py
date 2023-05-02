"""
Tests for social models.
"""

from django.test import TestCase
from djangoapps.social import models
from django.contrib.auth import get_user_model

class SocialModelTests(TestCase):
    """Test social models."""

    def test_profile_created_for_new_user(self):
        """Test that profile is always create for a new user."""
        email = 'test@example.com'
        username = 'test'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password
        )
        self.assertIsInstance(user.profile, Profile)