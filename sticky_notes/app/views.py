# app/views.py

from django.shortcuts import render, redirect, get_object_or_404

from .forms import *

from .models import *

from django.contrib.auth.decorators import login_required

from posts.models import *


# Code for the Home view
@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user)
    posts = Post.objects.filter(owner=request.user)
    return render(request, "home.html", {"tasks": tasks, "posts": posts})


# Code for the Create task view
@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("confirmation", task_id=task.id)
    else:
        form = TaskForm()
    return render(request, "create.html", {"form": form})


# Code for the Confirmation of task creation view
@login_required
def confirmation(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, "view.html", {"task": task})


# Code for Update task view
@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TaskForm(instance=task)
    return render(request, "update.html", {"form": form, "task": task})


# Code for Delete task view
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        task.delete()
        return redirect("home")


# Code for Viewing a task
@login_required
def view_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, "view.html", {"task": task})
