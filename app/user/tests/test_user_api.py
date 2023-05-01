"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

import logging
logger = logging.getLogger('my_logger')

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'username': 'TestName',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'username': 'TestName',
        }
        create_user(**payload)
        payload['username'] = 'TestName1'
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_username_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test0@example.com',
            'password': 'testpass123',
            'username': 'TestName',
        }
        create_user(**payload)
        payload['email'] = 'test1@example.com'
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        MIN_CHARS_IN_PASS = 5
        payload = {
            'email': 'test@example.com',
            'password': '',
            'name': 'Testname',
        }
        for i in range(MIN_CHARS_IN_PASS):
            payload['password'] = "a" * i

            res = self.client.post(CREATE_USER_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            user_exists = get_user_model().objects.filter(
                email=payload['email']
            ).exists()
            self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'username': 'Testname',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bed_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(email='test@example.com',
                    password='goodpass',
                    username='Testname',)

        payload = {'email': 'test@example.com','password':'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
