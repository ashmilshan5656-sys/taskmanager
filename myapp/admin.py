from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "due_date", "priority", "status")
    list_filter = ("priority", "status", "user")
    search_fields = ("title", "description")
