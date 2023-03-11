from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestAccount(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}

        self.credentials_invalid = {
            'username': 'testuser2',
            'password': 'secret1'}

        self.credentials_register = {
            'username': 'usertest',
            'password1': 'Mypassword123',
            'password2': 'Mypassword123'}

        self.credentials_register_invalid = {
            'username': 'usertest1',
            'password1': 'Mypassword1',
            'password2': 'Mypassword123'}

        User.objects.create_user(**self.credentials)

    def test_login(self):
        response_to_test_template = self.client.get(reverse('login'))
        response = self.client.post(
            reverse('login'), self.credentials)

        self.assertTemplateUsed(response_to_test_template,
                                'accounts/login.html')
        self.assertEqual(response.status_code, 200)

    def test_login_invalid(self):
        response_invalid = self.client.post(
            reverse('login'), self.credentials_invalid, follow=True)

        self.assertFalse(response_invalid.context['user'].is_authenticated)


    def test_logout(self):
        self.client.post(reverse('login'), self.credentials)
        response = self.client.post(reverse('logout'))

        self.assertEqual(response.status_code, 302)


    def test_register(self):
        response_to_test_template = self.client.get(reverse('register'))
        response = self.client.post(
            reverse('register'), data=self.credentials_register)

        self.assertTemplateUsed(
            response_to_test_template, template_name='accounts/register.html')

        self.assertEqual(response.status_code, 200)
        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 2)

    def test_register_invalid(self):
        response = self.client.post(
            reverse('register'), data=self.credentials_register_invalid)

        self.assertContains(
            response, "Unsuccessful registration. Invalid information.")
