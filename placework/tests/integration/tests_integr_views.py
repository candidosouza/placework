import re
from datetime import timedelta
from django.utils import timezone
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from placework.models import Profile, Address, PasswordResetCode


class HomeViewIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Olá, {self.user.get_full_name()}!')

    def test_unauthenticated_user(self):
        self.client.logout()
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Olá, Bem vindo ao PlaceWork!')


class LoginViewIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_authenticated_user_redirect(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/login/')
        self.assertRedirects(response, '/')

    def test_unauthenticated_user_get(self):
        self.client.logout()
        response = self.client.get('/login/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'form')
        self.assertContains(response, 'Email')
        self.assertContains(response, 'Senha')

    def test_unauthenticated_user_post_invalid(self):
        self.client.logout()

        response = self.client.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email ou senha inválidos.')

    def test_unauthenticated_user_post_invalid(self):
        self.client.logout()

        response = self.client.post('/login/', {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)


class RegisterUserViewIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='existinguser@example.com',
            password='testpassword'
        )

    def test_register_valid_user(self):
        """
        Testa o registro de um usuário válido.
        """
        data = {
            'username': 'newuser@example.com',
            'password': 'testpassword',
            'account_type': 'PF',
            'name': 'John Doe',
            'cpf': '123.456.789-09',
            'street': 'Teste Rua',
            'number': '456',
            'neighborhood': 'Bairro',
            'city': 'Cidade',
            'state': 'SP',
            'zip_code': '12345-678'
        }

        response = self.client.post(reverse('register'), data)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(User.objects.filter(username='newuser@example.com').exists())

    def test_register_existing_user(self):
        """
        Testa o registro de um usuário com um email já existente.
        """
        data = {
            'username': 'existinguser@example.com',
            'password': 'testpassword',
            'account_type': 'PF',
            'name': 'John Doe',
            'cpf': '123.456.789-09',
            'street': 'Rua Teste',
            'number': '456',
            'neighborhood': 'Bairro',
            'city': 'Cidade',
            'state': 'SP',
            'zip_code': '12345-678'
        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email já cadastrado.')

    def test_register_invalid_cpf(self):
        """
        Testa o registro de um usuário com um CPF inválido.
        """
        data = {
            'username': 'newuser@example.com',
            'password': 'testpassword',
            'account_type': 'PF',
            'name': 'John Doe',
            'cpf': '123.45',
            'street': 'Rua Teste',
            'number': '456',
            'neighborhood': 'Bairro Teste',
            'city': 'Cidade Teste',
            'state': 'SP',
            'zip_code': '12345-678'
        }

        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CPF inválido.')

    def test_register_with_cnpj(self):
        """
        Testa o registro de um usuário com CNPJ.
        """
        data = {
            'username': 'newbusiness@example.com',
            'password': 'testpassword',
            'account_type': 'PJ',
            'company_name': 'ACME Inc.',
            'cnpj': '96.093.720/0001-18',
            'street': 'Teste Rua',
            'number': '123',
            'neighborhood': 'Bairro Teste',
            'city': 'Cidade Teste',
            'state': 'SP',
            'zip_code': '98765-432'
        }

        response = self.client.post(reverse('register'), data)

        user = User.objects.filter(username='newbusiness@example.com').first()

        self.assertTrue(User.objects.filter(username='newbusiness@example.com').exists())
        self.assertTrue(Profile.objects.filter(cnpj='96.093.720/0001-18').exists())

    def test_register_blank_fields(self):
        """
        Testa o registro com campos em branco.
        """
        data = {
            'username': '',
            'password': 'testpassword',
            'account_type': 'PF',
            'name': '',
            'cpf': '123.456.789-09',
            'street': '',
            'number': '',
            'neighborhood': '',
            'city': '',
            'state': '',
            'zip_code': '',
        }

        response = self.client.post(reverse('register'), data)

        # print(response.context['form'].errors)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'street', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'number', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'neighborhood', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'city', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'state', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'zip_code', 'Este campo é obrigatório.')


class UpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
        )
        Profile.objects.create(
            user=self.user,
            account_type='PF',
            cpf='123.456.789-09',
            is_active=True
            )
        self.client.login(username='testuser@example.com', password='testpassword')

    def test_get_update_view(self):
        response = self.client.get(f'/alteracao-dados/{self.user.pk}/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'placework/update.html')
        self.assertContains(response, 'ALTERAR DADOS CADASTRAIS')

    def test_post_update_view(self):
        data = {
            'name': 'Updated User',
        }
        response = self.client.post(f'/alteracao-dados/{self.user.pk}/', data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')

    def test_post_update_view_invalid_password(self):
        data = {
            'name': '',
            'password': 'testpassword',
        }
        response = self.client.post(f'/alteracao-dados/{self.user.pk}/', data, follow=True)

        self.assertEqual(response.status_code, 200)
        data = {
            'name': 'Teste Update',
            'password': 'testpassword',
        }
        response = self.client.post(f'/alteracao-dados/{self.user.pk}/', data, follow=True)
        self.assertContains(response, 'A nova senha não pode corresponder a uma senha anterior.')

    def test_post_update_view_blank_name(self):
        data = {
            'name': '',
            'password': 'newpassword',
        }
        response = self.client.post(f'/alteracao-dados/{self.user.pk}/', data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dados Alterados com Sucesso!')


    def test_post_update_view_blank_password(self):
        data = {
            'name': 'Updated User',
            'password': '',  # Senha em branco
        }
        response = self.client.post(f'/alteracao-dados/{self.user.pk}/', data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')

    def test_post_update_view_invalid_form(self):
        data = {}
        response = self.client.post(f'/alteracao-dados/{self.user.pk}/', data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        data = {
            'name': 'Updated User',
            'password': 'newpassword',
            'nonexistent_field': 'value',
        }
        response = self.client.post(f'/alteracao-dados/{self.user.pk}/', data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_get_update_view_unauthenticated(self):
        self.client.logout()
        response = self.client.post(f'/alteracao-dados/99999/')
        self.assertEqual(response.status_code, 302)


class AddAddressViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser@example.com',
            password='testpassword',
        )
        self.client.login(username='testuser@example.com', password='testpassword')

    def test_get_add_address_view(self):
        response = self.client.get(f'/adicionar-endereco/{self.user.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'placework/add_address.html')
        self.assertContains(response, 'Adicionar Um Novo Endereço.')

    def test_post_add_address_view(self):
        data = {
            'street': 'Rua Teste',
            'number': 42,
            'complement': 'Apt 101',
            'neighborhood': 'Bairro Teste',
            'city': 'Cidade Teste',
            'state': 'SP',
            'zip_code': '12345-678',
        }
        response = self.client.post(f'/adicionar-endereco/{self.user.pk}/', data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

        self.assertTrue(Address.objects.filter(user=self.user, street='Rua Teste').exists())

    def test_post_add_address_view_invalid_data(self):
        data = {
            'street': 'Rua Teste',
            'number': '',
            'complement': 'Apt 101',
            'neighborhood': 'Bairro Teste',
            'city': 'Cidade Teste',
            'state': 'SP',
            'zip_code': '12345-678',
        }
        response = self.client.post(f'/adicionar-endereco/{self.user.pk}/', data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'placework/add_address.html')
        self.assertFormError(response, 'form', 'number', 'Este campo é obrigatório.')

    def test_post_add_address_view_unauthenticated(self):
        self.client.logout()
        data = {
            'street': 'Rua Teste',
            'number': 42,
            'complement': 'Apt 101',
            'neighborhood': 'Bairro Teste',
            'city': 'Cidade Teste',
            'state': 'SP',
            'zip_code': '12345-678',
        }
        response = self.client.post(f'/adicionar-endereco/{self.user.pk}/', data, follow=True)

        self.assertEqual(response.status_code, 404)


class CustomPasswordResetConfirmViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser@example.com',
            password='testpassword',
        )
        self.profile = Profile.objects.create(
            user=self.user,
            account_type='PF',
            cpf='123.456.789-09',
            is_active=True
        )
        self.reset_code = PasswordResetCode.objects.create(
            user=self.user,
            expiration_time=timezone.now() + timedelta(hours=1),
        )

    def test_valid_reset_code(self):
        response = self.client.get(f'/password_reset_confirm/{self.reset_code.code}', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_invalid_reset_code(self):
        response = self.client.get(f'/password_reset_confirm/xpto')
        self.assertEqual(response.status_code, 301)

    def test_expired_reset_code(self):
        expired_code = PasswordResetCode.objects.create(
            user=self.user,
            expiration_time=timezone.now() - timedelta(hours=1),
        )
        response = self.client.get(reverse('password_reset_confirm', kwargs={'uuid': str(expired_code.code)}))
        self.assertEqual(response.status_code, 302)


class PasswordResetViewTest(TestCase):

    def setUp(self):
        self.reset_url = reverse('password_reset')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_get_password_reset_page(self):
        response = self.client.get(self.reset_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'placework/password_reset.html')

    def test_valid_password_reset_request(self):
        data = {'email': 'test@example.com'}
        response = self.client.post(self.reset_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Um e-mail com instruções de recuperação de senha foi enviado para o seu endereço de e-mail.')

    def test_invalid_password_reset_request(self):
        data = {'email': 'nonexistent@example.com'}
        response = self.client.post(self.reset_url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Não há usuário cadastrado com este e-mail.')

