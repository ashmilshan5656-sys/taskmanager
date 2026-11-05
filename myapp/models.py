from django.conf import settings
from django.db import models


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("LOW", "LOW"),
        ("MEDIUM", "MEDIUM"),
        ("HIGH", "HIGH"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "PENDING"),
        ("COMPLETED", "COMPLETED"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks")

    class Meta:
        ordering = ["due_date", "-created_at"]

    def __str__(self):
        return self.title
