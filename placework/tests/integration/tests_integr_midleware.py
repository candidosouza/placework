import re
from profile import Profile

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.test import Client, TestCase, TransactionTestCase
from django.urls import reverse

from placework.middleware import CustomRedirectMiddleware
from placework.models import Profile


class CustomRedirectMiddlewareTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        Profile.objects.create(
            user=self.user,
            account_type='PF',
            cpf='12345678901',
            reset_password=True,
        )
        self.client = Client()

    def test_middleware_no_redirect(self):
        response = self.client.get(reverse('password_new'), follow=True)
        self.assertNotEqual(response.status_code, 302)
        self.assertEqual(response.status_code, 200)
