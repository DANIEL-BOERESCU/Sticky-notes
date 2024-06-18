# accounts/views.py

from django.shortcuts import render, redirect, HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout

from accounts.forms import RegisterForm, CustomAuthenticationForm

from django.contrib import messages


# Create your views here.


# Code for registering a new user
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            field, errors = list(form.errors.items())[0]
            error_message = f"Error in {field}: {errors[0]}"
            messages.error(request, error_message)
            return render(request, "accounts/register.html", {"form": form})
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


# Code for logging in an existing user
def user_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
                return HttpResponseRedirect(request.path_info)
        else:
            messages.error(request, "Invalid username or password.")
            return HttpResponseRedirect(request.path_info)
    else:
        form = CustomAuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


# Code for logout, with redirect to the login page
def user_logout(request):
    logout(request)
    return redirect("login")
