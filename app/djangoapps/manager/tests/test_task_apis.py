"""Tests for manager task APIs."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from djangoapps.manager.models import Task
from djangoapps.rpg.models import Character

from djangoapps.manager.serializers import (
    TaskSerializer,
    TaskDetailSerializer,
)


TASK_URL = reverse("manager:task-list")


def detail_url(task_id):
    """Return task url given Id."""
    return reverse("manager:task-detail", args=[task_id])


def create_user(
    email="user@example.com",
    password="testpass123",
    username="user",
):
    """Create and return user."""
    return get_user_model().objects.create_user(
        email=email, password=password, username=username
    )


def create_character(user, name="bob", **params):
    """Create and return character"""
    return Character.objects.create(user=user, name=name, **params)


def create_task(character, **params):
    """Create and return task."""
    defaults = {
        "title": "Eat",
        "content": "Eat a lot",
    }
    defaults.update(params)

    task = Task.objects.create(character=character, **defaults)
    return task


class PublicManagerTaskAPITests(TestCase):
    """Unauthenticated task API tests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required to access task APIs."""
        res = self.client.get(TASK_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateManagerTaskAPITests(TestCase):
    """Authenticated task API tests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.character = create_character(self.user, name="Rob")
        self.client.force_authenticate(self.user)

    def test_list_tasks(self):
        """Test user can get a list of their tasks."""
        create_task(self.character)
        create_task(self.character, title="Drink", content="Drink a lot.")

        res = self.client.get(TASK_URL)

        tasks = Task.objects.all().order_by("-id")
        serializer = TaskSerializer(tasks, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_task_list_limited_to_authenticated_user(self):
        """Test user can only get list of their tasks."""
        secondUser = create_user(email="user2@example.com", username="user2")
        secondChar = create_character(secondUser)
        create_task(self.character)
        create_task(secondChar, title="Drink", content="Drink a lot.")

        res = self.client.get(TASK_URL)

        tasks = Task.objects.filter(character=self.character).order_by("-id")
        serializer = TaskSerializer(tasks, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_task_detail(self):
        """Tests for retrieving task details."""
        task = create_task(character=self.character)

        url = detail_url(task.id)
        res = self.client.get(url)

        serializer = TaskDetailSerializer(task)
        self.assertEqual(res.data, serializer.data)

    def test_crete_task(self):
        """Test creating a task."""
        payload = {"title": "Eat", "content": "Eat a lot", "is_favorite": True}
        res = self.client.post(TASK_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get(id=res.data["id"])
        for k, v in payload.items():
            self.assertEqual(getattr(task, k), v)
        self.assertEqual(task.character, self.character)

    def test_partial_update(self):
        """Test updating task using PATCH method."""
        originalContent = "Eat a lot"
        task = create_task(self.character, content=originalContent)

        payload = {"title": "Eat food"}
        url = detail_url(task.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        task.refresh_from_db()

        self.assertEqual(task.title, payload["title"])
        self.assertEqual(task.content, originalContent)

    def test_update_character_returns_error(self):
        """Test trying to update character on the task returns error."""
        secondUser = create_user(email="user2@example.com", username="user2")
        secondChar = create_character(secondUser)
        task = create_task(self.character)

        payload = {"character": secondChar.id}
        url = detail_url(task.id)
        self.client.patch(url, payload)

        task.refresh_from_db()
        self.assertEqual(task.character, self.character)

    def test_delete_task_successful(self):
        """Test deleting task is successful."""
        task = Task.objects.create(character=self.character)

        url = detail_url(task.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_delete_other_character_task_error(self):
        """Test deleting other characters task creates error."""
        secondUser = create_user(email="user2@example.com", username="user2")
        secondChar = create_character(secondUser)
        task = create_task(secondChar)

        url = detail_url(task.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Task.objects.filter(id=task.id).exists())
