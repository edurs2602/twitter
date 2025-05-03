from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from follow.models import Follow

User = get_user_model()


class TestFollowViewSet(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='password123', email='user2@example.com')

        refresh = RefreshToken.for_user(self.user1)
        self.token = str(refresh.access_token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_follow_user(self):
        url = reverse('follow_user', kwargs={'pk': self.user2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Follow.objects.filter(user=self.user1, following_user=self.user2).exists())

    def test_unfollow_user(self):
        Follow.objects.create(user=self.user1, following_user=self.user2)
        url = reverse('unfollow_user', kwargs={'pk': self.user2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Follow.objects.filter(user=self.user1, following_user=self.user2).exists())

    def test_following_count(self):
        Follow.objects.create(user=self.user1, following_user=self.user2)
        url = reverse('count_following', kwargs={'pk': self.user1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['following_count'], 1)

    def test_followers_count(self):
        Follow.objects.create(user=self.user1, following_user=self.user2)
        url = reverse('count_followers', kwargs={'pk': self.user2.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['followers_count'], 1)
