# app/models.py

from django.db import models
from django.contrib.auth.models import User


# code for the Task class model
class Task(models.Model):
    STATUS_CHOICES = (
        ("To Do", "To Do"),
        ("In Progress", "In Progress"),
        ("Personal", "Personal"),
        ("Completed", "Completed"),
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="todo"
    )

    def __str__(self):
        return self.title
