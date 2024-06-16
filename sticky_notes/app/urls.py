# app/urls.py

from django.contrib import admin

from django.urls import path

from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("create_task/", views.create_task, name="create_task"),
    path("confirmation/", views.confirmation, name="confirmation"),
    path("update_task/<int:task_id>/", views.update_task, name="update_task"),
    path("delete_taskk/<int:task_id>/", views.delete_task, name="delete_task"),
    path("view/<int:task_id>/", views.view_task, name="view_task"),
    path("confirmation/<int:task_id>/", views.confirmation, name="confirmation"),
]
