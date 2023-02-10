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

    """Test to make sure a user has to  be logged in to create a post."""
    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        christian = User.objects.create_user(
            username='christian', password='pass'
        )
        nils = User.objects.create_user(
            username='nils', password='pass'
        )
        Post.objects.create(
            owner=christian, title='a title', content='christians content'
        )
        Post.objects.create(
            owner=nils, title='another title', content='nils content'
        )

    """Test if it's possible to retrieve a post with a valid ID."""
    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """Test if it's possible to retrieve a post with an invalid ID."""
    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    """Test to see that users can update posts that  they own."""
    def test_user_can_update_own_post(self):
        self.client.login(username='christian', password='pass')
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """Test to see that even if we're logged in, we can't
    edit a post that we don't own."""
    def test_user_cant_update_another_users_post(self):
        self.client.login(username='christian', password='pass')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
