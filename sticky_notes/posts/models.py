# posts/models.py

from django.db import models
from django.contrib.auth.models import User


# Code for the Post class model
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="app_posts"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
