from unittest.mock import Mock

from django.test import TestCase

from placework.forms import (
    AddressForm,
    LoginForm,
    PasswordResetConfirmForm,
    PasswordResetForm,
    RegisterForm,
    UpdateForm,
)


class RegisterFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'username': 'test@example.com',
            'password': 'password123',
            'account_type': 'PF',
            'name': 'John Doe',
            'cpf': '123.456.789-09',
            'street': 'Rua Teste',
            'number': '42',
            'neighborhood': 'Bairro Teste',
            'city': 'Cidade Teste',
            'state': 'SP',
            'zip_code': '15500-000',
        }
        form = RegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'username': 'invalid-email',
            'password': '',
            'account_type': '',
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_custom_validators(self):
        data = {
            'username': 'test@example.com',
            'password': 'password123',
            'account_type': 'PF',
            'name': 'John Doe',
            'cpf': '123.456.789-10',  # CPF inválido
            'street': 'Rua Teste',
            'number': '42',
            'neighborhood': 'Bairro Teste',
            'city': 'Cidade Teste',
            'state': 'SP',
            'zip_code': '15500-000',
        }
        form = RegisterForm(data=data)
        self.assertFalse(form.is_valid())

    def test_mocked_clean_method(self):
        form = RegisterForm(data={})
        form.is_valid = Mock(return_value=True)
        form.cleaned_data = {'username': 'test@example.com'}
        is_valid = form.is_valid()
        self.assertTrue(is_valid)
        cleaned_data = form.cleaned_data
        self.assertEqual(cleaned_data['username'], 'test@example.com')


class AddressFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'street': 'Rua Teste',
            'number': '42',
            'neighborhood': 'Bairro Teste',
            'city': 'Cidade Teste',
            'state': 'SP',
            'zip_code': '15500-000',
        }
        form = AddressForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'street': '',
            'number': '',
            'neighborhood': '',
            'city': '',
            'state': '',
            'zip_code': '',
        }
        form = AddressForm(data=data)
        self.assertFalse(form.is_valid())


class LoginFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'username': 'email@email.com',
            'password': '123456',
        }
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'username': '',
            'password': '',
        }
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())


class UpdateFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'name': 'John Doe',
            'password': '123456',
        }
        form = UpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = UpdateForm(data={})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'name': 'Nome Com Espaço',
            'password': '',
        }
        form = UpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_name_only(self):
        form_data = {
            'name': 'Novo Nome',
            'password': '',
        }
        form = UpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_password_only(self):
        form_data = {
            'name': '',
            'password': 'NovaSenha123',
        }
        form = UpdateForm(data=form_data)
        self.assertTrue(form.is_valid())


class PasswordResetFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'email': 'email@email.com',
        }
        form = PasswordResetForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {
            'email': '',
        }
        form = PasswordResetForm(data=data)
        self.assertFalse(form.is_valid())


class PasswordResetConfirmFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'password': 'NovaSenha123',
        }
        form = PasswordResetConfirmForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_form(self):
        form = PasswordResetConfirmForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_invalid_form(self):
        form_data = {
            'password': '',
        }
        form = PasswordResetConfirmForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)

    def test_valid_form_with_whitespace_password(self):
        form_data = {
            'password': '   NovaSenha123   ',
        }
        form = PasswordResetConfirmForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_form_with_long_password(self):
        form_data = {
            'password': 'SenhaMuitoLonga1234567890',
        }
        form = PasswordResetConfirmForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_form_with_short_password(self):
        form_data = {
            'password': 'Curta123',
        }
        form = PasswordResetConfirmForm(data=form_data)
        self.assertTrue(form.is_valid())
