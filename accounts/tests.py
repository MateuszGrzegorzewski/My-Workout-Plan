from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CustomUser


class LoginTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpassword'
        )
        self.url = reverse('login')

    def test_successful_login(self):
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_wrong_credentials(self):
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_missing_email_or_password(self):
        data = {'email': 'test@example.com'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

        data = {'password': 'testpassword'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_non_existing_email(self):
        data = {'email': 'nonexisting@example.com', 'password': 'testpassword'}
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserRegistrationTests(APITestCase):

    def test_valid_registration(self):
        url = reverse('register')

        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().email,
                         'test@example.com')

    def test_registration_with_existing_email(self):
        get_user_model().objects.create_user(
            email='test@example.com', password='password123')

        url = reverse('register')

        data = {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_missing_email(self):
        url = reverse('register')

        data = {
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0], 'This field is required.')

    def test_registration_with_missing_password(self):
        url = reverse('register')

        data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password']
                         [0], 'This field is required.')


class CustomUserModelTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@test.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User"
        }
        self.user = CustomUser.objects.create_user(**self.user_data)

    def test_custom_user_creation(self):
        self.assertEqual(self.user_data["email"], str(self.user))

    def test_create_user_with_valid_email_and_password(self):
        email = "test@example.com"
        password = "testpassword123"
        user = CustomUser.objects.create_user(email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser_with_valid_email_and_password(self):
        email = "test@example.com"
        password = "testpassword123"
        user = CustomUser.objects.create_superuser(
            email=email, password=password, is_staff=True, is_superuser=True)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser_missing_fields(self):
        with self.assertRaises(ValueError) as cm:
            CustomUser.objects.create_superuser(
                email='test@test.com',
                password='password',
                is_staff=False,
                is_superuser=True,
            )

        self.assertEqual(str(cm.exception),
                         'Superuser must have is_staff = True')

        with self.assertRaises(ValueError) as cm:
            CustomUser.objects.create_superuser(
                email='test@test.com',
                password='password',
                is_staff=True,
                is_superuser=False,
            )

        self.assertEqual(str(cm.exception),
                         'Superuser must have is_superuser = True')
