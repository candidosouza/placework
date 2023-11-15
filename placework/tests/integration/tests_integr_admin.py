from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase

from placework.models import Address, Profile


class AdminTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            first_name='John',
            last_name='Doe',
        )
        self.profile = Profile.objects.create(
            user=self.user, account_type='PF', cpf='12345678901'
        )
        self.address = Address.objects.create(
            user=self.user,
            street='Rua Teste',
            number=42,
            complement='',
            neighborhood='Bairro Teste',
            city='Cidade Teste',
            state='SP',
            zip_code='15500-000',
        )

    def test_user_admin(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            f'/admin-placework/auth/user/{self.user.id}/change/'
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Perfil')
        self.assertContains(response, 'Endereço')
        self.assertContains(response, 'CPF')
        self.assertContains(response, 'CNPJ')
        self.assertContains(response, 'Rua')
        self.assertContains(response, 'Número')
        self.assertContains(response, 'Complemento')
        self.assertContains(response, 'Bairro')
        self.assertContains(response, 'Cidade')
        self.assertContains(response, 'Estado')
        self.assertContains(response, 'CEP')

    def test_user_admin_search(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            '/admin-placework/auth/user/', {'q': 'John Doe'}
        )
        self.assertEqual(response.status_code, 200)
