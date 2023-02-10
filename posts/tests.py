from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    """First, we'll define the setUp method that will automatically
    run before every test method in the class. Inside, I'll create a
    user that we can reference later on in all the tests inside this class.
    We'll use this user's credentials when we need to log in to
    create a post."""
    def setUp(self):
        User.objects.create_user(username='christian', password='pass')

    """Test that we can list posts present in the database."""
    def test_can_list_posts(self):
        christian = User.objects.get(username='christian')
        Post.objects.create(owner=christian, title='a title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    """Test to make sure that a  logged in user can create a post."""
    def test_logged_in_user_can_create_post(self):
        self.client.login(username='christian', password='pass')
        response = self.client.post('/posts/', {'title': 'a title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
