# posts/urls.py

from django.urls import path

from posts import views

urlpatterns = [
    path("create_post/", views.create_post, name="create_post"),
    path("view_post/<int:id>/", views.view_post, name="view_post"),
    path("update_post/<int:id>/edit/", views.update_post, name="update_post"),
    path(
        "delete_post/<int:id>/delete/", views.delete_post, name="delete_post"
    ),
]
