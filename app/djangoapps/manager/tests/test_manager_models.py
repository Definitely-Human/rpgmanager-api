"""Test for manager app models."""

from django.test import TestCase
from djangoapps.manager.models import (
    Task,
    Tag,
    Category,
)
from djangoapps.rpg.models import Character
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError


def create_user(
    email="user@example.com",
    password="testpass123",
    username="user",
):
    """Create and return user."""
    return get_user_model().objects.create_user(
        email=email, password=password, username=username
    )


class ManagerTaskTests(TestCase):
    """Tests for manager task model."""

    def test_create_new_task(self):
        """Test creating new task."""
        user = create_user()
        character = Character.objects.create(user=user, name="Bob")
        task = Task.objects.create(
            character=character, title="Eat", content="Eat a lot"
        )
        self.assertEqual(str(task), task.title)


class ManagerTagTests(TestCase):
    """Tests for manager tag model."""

    def setUp(self):
        self.user = create_user(email="user0@example.com", username="user0")

    def test_create_new_tag(self):
        """Test creating new tag is successful."""
        tag = Tag.objects.create(user=self.user, name="Eating")

        self.assertEqual(str(tag), tag.name)

    def test_user_can_not_create_tags_with_same_name(self):
        tag = Tag.objects.create(user=self.user, name="Eating")

        self.assertRaises(
            IntegrityError,
            Tag.objects.create,
            user=self.user,
            name="Eating",
        )

    def test_different_users_can_create_tags_with_same_name(self):
        tag = Tag.objects.create(user=self.user, name="Eating")
        other_user = create_user()
        other_tag = Tag.objects.create(user=other_user, name="Eating")

        tag.refresh_from_db()
        other_tag.refresh_from_db()

        self.assertEqual(tag.user, self.user)
        self.assertEqual(other_tag.user, other_user)


class ManagerCategoryTests(TestCase):
    """Tests for manager category model."""

    def test_create_new_category(self):
        """Test creating new category is successful."""
        user = create_user()
        category = Category.objects.create(user=user, name="Eating")

        self.assertEqual(str(category), category.name)
