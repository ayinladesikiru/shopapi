from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class RegisterViewTests(APITestCase):
    url = reverse('register')

    def setUp(self):
        self.valid_payload = {
            'email': 'ada@example.com',
            'password': 'StrongPass123!',
            'first_name': 'Ada',
            'last_name': 'Lovelace',
            'phone': '08012345678',
            'username': 'ada',
        }

    def test_register_creates_user(self):
        response = self.client.post(self.url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='ada@example.com').exists())
        self.assertEqual(response.data['email'], 'ada@example.com')
        self.assertEqual(response.data['username'], 'ada')

    def test_password_not_returned_in_response(self):
        response = self.client.post(self.url, self.valid_payload, format='json')

        self.assertNotIn('password', response.data)

    def test_password_is_hashed(self):
        self.client.post(self.url, self.valid_payload, format='json')

        user = User.objects.get(email='ada@example.com')
        self.assertNotEqual(user.password, self.valid_payload['password'])
        self.assertTrue(user.check_password(self.valid_payload['password']))

    def test_duplicate_email_rejected(self):
        self.client.post(self.url, self.valid_payload, format='json')
        payload = {**self.valid_payload, 'username': 'ada2'}

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_duplicate_username_rejected(self):
        self.client.post(self.url, self.valid_payload, format='json')
        payload = {**self.valid_payload, 'email': 'other@example.com'}

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_missing_required_fields_rejected(self):
        for field in ['email', 'password', 'username', 'phone']:
            with self.subTest(field=field):
                payload = {k: v for k, v in self.valid_payload.items() if k != field}

                response = self.client.post(self.url, payload, format='json')

                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field, response.data)

    def test_invalid_email_rejected(self):
        payload = {**self.valid_payload, 'email': 'not-an-email'}

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
