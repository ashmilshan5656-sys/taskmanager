from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("tasks/", views.task_list, name="task_list"),
    path("tasks/create/", views.task_create, name="task_create"),
    path("tasks/edit/<int:pk>/", views.task_edit, name="task_edit"),
    path("tasks/delete/<int:pk>/", views.task_delete, name="task_delete"),
]
