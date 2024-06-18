# posts/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from posts.models import Post


class TaskAndPostTests(TestCase):
    # Create a setup function to facilitate testing
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = Client()
        self.client.login(username="testuser", password="testpassword")

        # Create a sample post
        self.post = Post.objects.create(
            owner=self.user,
            title="Sample Post",
            content="This is a sample Post Content.",
        )

    # Test for creating a post
    def test_create_post_view(self):
        response = self.client.get(reverse("create_post"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create.html")

        response = self.client.post(
            reverse("create_post"),
            {"title": "New Post", "content": "This is a new post content."},
        )
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertTrue(Post.objects.filter(title="New Post").exists())

    # Test for updating a post
    def test_update_post_view(self):
        response = self.client.get(reverse("update_post", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update.html")

        response = self.client.post(
            reverse("update_post", args=[self.post.id]),
            {
                "title": "Updated Post",
                "content": "This is an updated post content.",
            },
        )
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        updated_post = Post.objects.get(id=self.post.id)
        self.assertEqual(updated_post.title, "Updated Post")

    # Test for deleting a post
    def test_delete_post_view(self):
        response = self.client.post(
            reverse("delete_post", args=[self.post.id])
        )
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=self.post.id)

    # Test for viewing a post
    def test_view_post_view(self):
        response = self.client.get(reverse("view_post", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "view.html")
        self.assertEqual(response.context["post"].title, "Sample Post")
