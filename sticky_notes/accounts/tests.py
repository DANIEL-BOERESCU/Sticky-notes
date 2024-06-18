# accounts/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


# code for testing the Register functionality
class RegisterViewTest(TestCase):
    def test_register_view(self):
        user_data = {
            "username": "testuser",
            "email": "test@gmail.com",
            "password1": "testpassword1",
            "password2": "testpassword1",
        }

        response = self.client.post(reverse("register"), user_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="testuser").exists())


# code for testing the Login functionality
class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword1",
            email="test@example.com",
        )

    def test_login_view(self):
        login_data = {"username": "testuser", "password": "testpassword1"}

        response = self.client.post(reverse("login"), login_data)
        self.assertEqual(response.status_code, 302)


# code for testing the Logout functionality
class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword1",
            email="test@example.com",
        )

    def test_logout_view(self):
        self.client.login(username="testuser", password="testpassword1")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))
