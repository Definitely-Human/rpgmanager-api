"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        username = "test"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email, username=username, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@Example.COM", "TEST3@example.com"],
            ["test4@Example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            username = expected[:5]
            user = get_user_model().objects.create_user(
                email, username, "sample123"
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """
        Test that creating a user without an email raises a Value Error.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                "",
                "testusername",
                "test123",
            )

    def test_new_user_without_username_raises_error(self):
        """
        Test that creating a user without an username raises a Value Error.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                "test@example.com",
                "",
                "test123",
            )

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "testusername",
            "test123",
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
