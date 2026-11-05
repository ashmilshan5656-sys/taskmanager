from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegistrationForm, TaskForm
from .models import Task


def home(request):
    if request.user.is_authenticated:
        return redirect("task_list")
    return redirect("login")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("task_list")
    else:
        form = RegistrationForm()
    return render(request, "myapp/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("task_list")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            next_url = request.GET.get("next") or "task_list"
            return redirect(next_url)
    else:
        form = AuthenticationForm()

    return render(request, "myapp/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, "myapp/task_list.html", {"tasks": tasks})


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "myapp/task_form.html", {"form": form, "mode": "Create"})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "myapp/task_form.html", {"form": form, "mode": "Edit"})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    return render(request, "myapp/task_delete.html", {"task": task})
