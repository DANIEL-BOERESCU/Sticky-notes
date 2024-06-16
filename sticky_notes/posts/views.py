# posts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required


# Code for creating a post
@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "create.html", {"form": form})


# Code for viewing a post
def view_post(request, id):
    post = get_object_or_404(Post, id=id, owner=request.user)
    return render(request, "view.html", {"post": post})


# Code for updating a post
def update_post(request, id):
    post = get_object_or_404(Post, id=id, owner=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PostForm(instance=post)
    return render(request, "update.html", {"form": form})


# Code for deleting a post
def delete_post(request, id):
    post = get_object_or_404(Post, id=id, owner=request.user)
    if request.method == "POST":
        post.delete()
        return redirect("home")
    return render(request, "delete_post.html", {"post": post})
