# user/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class TestUserViewSet(TestCase):

    def test_user_creation(self):
        url = reverse('user-list')
        data = {
            'username': 'testuser',
            'password': 'password123',
            'email': 'testuser@example.com'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_creation_invalid_data(self):
        url = reverse('user-list')
        data = {
            'username': 'testuser',
            'password': 'password123',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('email', response.data)
