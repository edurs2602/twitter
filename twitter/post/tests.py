from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from post.models import Post

User = get_user_model()

class TestPostViewSet(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123', email='user1@example.com')
        refresh = RefreshToken.for_user(self.user1)
        self.token = str(refresh.access_token)

        self.client = APIClient()  # Usando o APIClient
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_post(self):
        url = reverse('post-list')  # URL para criar post
        data = {
            'text': 'This is a test post.',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Post.objects.filter(user=self.user1, text='This is a test post.').exists())

    def test_like_post(self):
        post = Post.objects.create(user=self.user1, text='This is a post to like.')
        url = reverse('post-like', kwargs={'pk': post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertTrue(post.likes.filter(id=self.user1.id).exists())

    def test_unlike_post(self):
        post = Post.objects.create(user=self.user1, text='This is a post to like.')
        post.likes.add(self.user1)
        url = reverse('post-unlike', kwargs={'pk': post.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertFalse(post.likes.filter(id=self.user1.id).exists())
