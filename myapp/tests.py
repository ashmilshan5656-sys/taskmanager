from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="alice", password="secret123")
        self.other_user = get_user_model().objects.create_user(username="bob", password="secret123")
        self.task = Task.objects.create(
            title="Write report",
            description="Draft the project summary",
            due_date=date(2026, 10, 15),
            priority="HIGH",
            status="PENDING",
            user=self.user,
        )

    def test_user_sees_only_their_own_tasks(self):
        self.client.login(username="alice", password="secret123")
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Write report")

    def test_user_cannot_access_another_users_task(self):
        other_task = Task.objects.create(
            title="Other task",
            description="another user task",
            due_date=date(2026, 10, 20),
            priority="LOW",
            status="PENDING",
            user=self.other_user,
        )
        self.client.login(username="alice", password="secret123")
        response = self.client.get(reverse("task_edit", args=[other_task.pk]))
        self.assertEqual(response.status_code, 404)
