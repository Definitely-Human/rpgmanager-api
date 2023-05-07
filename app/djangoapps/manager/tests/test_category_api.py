"""Tests for category API."""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from djangoapps.manager.models import Category
from djangoapps.manager.serializers import CategorySerializer


CATEGORY_URL = reverse("manager:category-list")


def detail_url(category_id):
    """Get category detail URL."""
    return reverse("manager:category-detail", args=[category_id])


def create_user(
    email="user@example.com",
    password="testpass123",
    username="user",
):
    """Create and return user."""
    return get_user_model().objects.create_user(
        email=email, password=password, username=username
    )


def create_category(user, name="Eating"):
    """Create and return category."""
    return Category.objects.create(user=user, name=name)


class PublicCategoryAPITests(TestCase):
    """Unauthenticated tests for category APIs."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required to access category API."""
        res = self.client.get(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoryAPITests(TestCase):
    """Authenticated tests for category APIs."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="user0@example.com", username="user0")
        self.client.force_authenticate(self.user)

    def test_get_category_list(self):
        """Test getting a list of categories."""
        Category.objects.create(user=self.user)
        Category.objects.create(user=self.user, name="Training")

        res = self.client.get(CATEGORY_URL)

        categories = Category.objects.all().order_by("name")
        serializer = CategorySerializer(categories, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_categories_limited_to_user(self):
        """Test list of categories limited to authenticated user."""
        user2 = create_user()
        create_category(user2)
        category = create_category(self.user, name="Training")

        res = self.client.get(CATEGORY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], category.name)
        self.assertEqual(res.data[0]["id"], category.id)
