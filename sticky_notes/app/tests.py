# app/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from app.models import Task
from datetime import date


class TaskTests(TestCase):
    # Create a setup function to facilitate testing
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")

        self.task = Task.objects.create(
            user=self.user,
            title="Sample Task",
            description="This is a sample task description.",
            deadline=date(2024, 12, 31),
            status="To Do",
        )

    # Test task creation
    def test_task_creation(self):
        response = self.client.get(reverse("create_task"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create.html")

        response = self.client.post(
            reverse("create_task"),
            {
                "title": "New Task",
                "description": "This is a new task description.",
                "deadline": "2024-12-31",
                "status": "To Do",
            },
        )
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue(Task.objects.filter(title="New Task").exists())

    # Test task updating
    def test_task_update(self):
        response = self.client.get(reverse("update_task", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update.html")

        response = self.client.post(
            reverse("update_task", args=[self.task.id]),
            {
                "title": "Updated Task",
                "description": "This is an updated task description.",
                "deadline": "2024-12-31",
                "status": "To Do",
            },
        )
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")

    # Test task deletion
    def test_task_deletion(self):
        response = self.client.post(
            reverse("delete_task", args=[self.task.id])
        )
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task.id)

    # Test task viewing
    def test_task_view(self):
        response = self.client.get(reverse("view_task", args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "view.html")
        self.assertContains(response, self.task.title)
