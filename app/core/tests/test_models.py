"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def ftest_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        username = 'test'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            username=username,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def ftest_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@Example.COM', 'TEST3@example.com'],
            ['test4@Example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            username = expected[:5]
            user = get_user_model().objects.create_user(email, username, 'sample123')
            self.assertEqual(user.email, expected)
