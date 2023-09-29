from django.contrib import admin
from django.contrib.auth.models import User
from django.test import TestCase

from placework.models import Address, Profile


class AdminTest(TestCase):
    def setUp(self):
        # Crie um usuário de exemplo
        self.user = User.objects.create_superuser(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            first_name='John',
            last_name='Doe',
        )

        # Crie um perfil de exemplo
        self.profile = Profile.objects.create(
            user=self.user, account_type='PF', cpf_cnpj='12345678901'
        )

        # Crie um endereço de exemplo
        self.address = Address.objects.create(
            user=self.user,
            street='123 Main St',
            number=42,
            complement='',
            neighborhood='Downtown',
            city='Exampleville',
            state='EX',
            country='US',
            zip_code='12345',
        )

    def test_user_admin(self):
        # Verifique se o usuário está logado no admin
        self.client.login(username='testuser', password='testpassword')

        # Acesse a página de alteração de usuário
        response = self.client.get(f'/admin/auth/user/{self.user.id}/change/')

        # Verifique se a resposta é bem-sucedida
        self.assertEqual(response.status_code, 200)

        # Verifique se os campos personalizados do perfil e do endereço estão presentes
        self.assertContains(response, 'Perfil')
        self.assertContains(response, 'Endereço')

        # Verifique se os campos de perfil e endereço estão presentes
        self.assertContains(response, 'CPF/CNPJ')
        self.assertContains(response, 'Rua')
        self.assertContains(response, 'Número')
        self.assertContains(response, 'Complemento')
        self.assertContains(response, 'Bairro')
        self.assertContains(response, 'Cidade')
        self.assertContains(response, 'Estado')
        self.assertContains(response, 'País')
        self.assertContains(response, 'CEP')

    def test_user_admin_search(self):
        # Verifique se o usuário está logado no admin
        self.client.login(username='testuser', password='testpassword')

        # Pesquise por um usuário com base no nome do perfil
        response = self.client.get('/admin/auth/user/', {'q': 'John Doe'})

        # Verifique se a resposta é bem-sucedida
        self.assertEqual(response.status_code, 200)

        # Verifique se o usuário é encontrado na pesquisa
        # self.assertContains(response, 'test@example.com')
