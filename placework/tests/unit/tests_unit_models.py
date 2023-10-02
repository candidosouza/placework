from datetime import timedelta
from django.utils import timezone
import uuid
from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase

from placework.models import Address, Profile, EmailActivation, PasswordResetCode, PasswordHistory


class ProfileModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        Profile.objects.create(
            user=self.user,
            account_type='PF',
            cpf='12345678901',
        )

    def test_user_label(self):
        profile = Profile.objects.get(user=self.user)
        field_label = profile._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_account_type_label(self):
        profile = Profile.objects.get(user=self.user)
        field_label = profile._meta.get_field('account_type').verbose_name
        self.assertEqual(field_label, 'Tipo de conta')

    def test_is_active_label(self):
        profile = Profile.objects.get(user=self.user)
        field_label = profile._meta.get_field('is_active').verbose_name
        self.assertEqual(field_label, 'Ativo')

    def test_cpf_label(self):
        profile = Profile.objects.get(user=self.user)
        field_label = profile._meta.get_field('cpf').verbose_name
        self.assertEqual(field_label, 'CPF')
    
    def test_cnpj_label(self):
        profile = Profile.objects.get(user=self.user)
        field_label = profile._meta.get_field('cnpj').verbose_name
        self.assertEqual(field_label, 'CNPJ')

    def test_account_type_choices(self):
        profile = Profile.objects.get(user=self.user)
        choices = profile._meta.get_field('account_type').choices
        self.assertEqual(choices, (('PF', 'PF'), ('PJ', 'PJ')))

    def test_is_active_default(self):
        profile = Profile.objects.get(user=self.user)
        default_value = profile._meta.get_field('is_active').default
        self.assertEqual(default_value, False)

    def test_profile_str_method(self):
        profile = Profile.objects.get(user=self.user)
        expected_str = f'{profile.user.username}'
        self.assertEqual(str(profile), expected_str)

    def test_class__meta__(self):
        self.assertEqual(str(Profile._meta), 'placework.profile')

    def test_verbose_name(self):
        self.assertEqual(str(Profile._meta.verbose_name), 'Perfil')
        self.assertEqual(str(Profile._meta.verbose_name_plural), 'Perfis')

    def test_mapping(self):
        table_name = Profile._meta.db_table
        self.assertEqual(table_name, 'placework_profile')

        fields_name = tuple(field.name for field in Profile._meta.fields)
        self.assertEqual(
            fields_name,
            ('id', 'user', 'account_type', 'is_active', 'company_name', 'cpf', 'cnpj', 'error_login', 'is_blocked', 'reset_password')
        )

        user_field: models.ForeignKey = Profile.user.field
        self.assertIsInstance(user_field, models.ForeignKey)
        self.assertFalse(user_field.null)
        self.assertFalse(user_field.blank)
        self.assertIsNone(user_field.db_column)
        self.assertTrue(user_field.editable)

        account_type_field: models.CharField = Profile.account_type.field
        self.assertIsInstance(account_type_field, models.CharField)
        self.assertFalse(account_type_field.null)
        self.assertFalse(account_type_field.blank)
        self.assertIsNone(account_type_field.db_column)
        self.assertTrue(account_type_field.editable)
        self.assertEqual(account_type_field.max_length, 2)

        is_active_field: models.BooleanField = Profile.is_active.field
        self.assertIsInstance(is_active_field, models.BooleanField)
        self.assertIsNone(is_active_field.db_column)
        self.assertTrue(is_active_field.editable)

        cpf_field: models.CharField = Profile.cpf.field
        self.assertIsInstance(cpf_field, models.CharField)
        self.assertTrue(cpf_field.null)
        self.assertTrue(cpf_field.blank)
        self.assertIsNone(cpf_field.db_column)
        self.assertTrue(cpf_field.editable)
        self.assertEqual(cpf_field.max_length, 14)

        cnpj_field: models.CharField = Profile.cnpj.field
        self.assertIsInstance(cnpj_field, models.CharField)
        self.assertTrue(cnpj_field.null)
        self.assertTrue(cnpj_field.blank)
        self.assertIsNone(cnpj_field.db_column)
        self.assertTrue(cnpj_field.editable)
        self.assertEqual(cnpj_field.max_length, 18)


class AddressModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        Address.objects.create(
            user=self.user,
            street='Rua Teste',
            number=42,
            complement='Apt 3B',
            neighborhood='Bairro Teste',
            city='Cidade Teste',
            state='SP',
            zip_code='12345678',
        )

    def test_user_label(self):
        address = Address.objects.get(user=self.user)
        field_label = address._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_street_label(self):
        address = Address.objects.get(user=self.user)
        field_label = address._meta.get_field('street').verbose_name
        self.assertEqual(field_label, 'Rua')

    def test_number_label(self):
        address = Address.objects.get(user=self.user)
        field_label = address._meta.get_field('number').verbose_name
        self.assertEqual(field_label, 'Número')

    def test_complement_label(self):
        address = Address.objects.get(user=self.user)
        field_label = address._meta.get_field('complement').verbose_name
        self.assertEqual(field_label, 'Complemento')

    def test_neighborhood_label(self):
        address = Address.objects.get(user=self.user)
        field_label = address._meta.get_field('neighborhood').verbose_name
        self.assertEqual(field_label, 'Bairro')

    def test_city_label(self):
        address = Address.objects.get(user=self.user)
        field_label = address._meta.get_field('city').verbose_name
        self.assertEqual(field_label, 'Cidade')

    def test_state_label(self):
        address = Address.objects.get(user=self.user)
        field_label = address._meta.get_field('state').verbose_name
        self.assertEqual(field_label, 'Estado')

    def test_zip_code_label(self):
        address = Address.objects.get(user=self.user)
        field_label = address._meta.get_field('zip_code').verbose_name
        self.assertEqual(field_label, 'CEP')

    def test_address_str_method(self):
        address = Address.objects.get(user=self.user)
        expected_str = f'{address.street}, {address.number}, {address.city}, {address.state}'
        self.assertEqual(str(address), expected_str)

    def test_class__meta__(self):
        self.assertEqual(str(Address._meta), 'placework.address')

    def test_verbose_name(self):
        self.assertEqual(str(Address._meta.verbose_name), 'Endereço')
        self.assertEqual(str(Address._meta.verbose_name_plural), 'Endereços')

    def test_mapping(self):
        table_name = Address._meta.db_table
        self.assertEqual(table_name, 'placework_address')

        fields_name = tuple(field.name for field in Address._meta.fields)
        self.assertEqual(
            fields_name,
            (
                'id',
                'user',
                'street',
                'number',
                'complement',
                'neighborhood',
                'city',
                'state',
                'zip_code',
            ),
        )

        user_field: models.ForeignKey = Address.user.field
        self.assertIsInstance(user_field, models.ForeignKey)
        self.assertFalse(user_field.null)
        self.assertFalse(user_field.blank)
        self.assertIsNone(user_field.db_column)
        self.assertTrue(user_field.editable)

        street_field: models.CharField = Address.street.field
        self.assertIsInstance(street_field, models.CharField)
        self.assertFalse(street_field.null)
        self.assertFalse(street_field.blank)
        self.assertIsNone(street_field.db_column)
        self.assertTrue(street_field.editable)
        self.assertEqual(street_field.max_length, 255)

        number_field: models.IntegerField = Address.number.field
        self.assertIsInstance(number_field, models.IntegerField)
        self.assertFalse(number_field.null)
        self.assertFalse(number_field.blank)
        self.assertIsNone(number_field.db_column)
        self.assertTrue(number_field.editable)

        complement_field: models.CharField = Address.complement.field
        self.assertIsInstance(complement_field, models.CharField)
        self.assertTrue(complement_field.null)
        self.assertTrue(complement_field.blank)
        self.assertIsNone(complement_field.db_column)
        self.assertTrue(complement_field.editable)
        self.assertEqual(complement_field.max_length, 255)

        neighborhood_field: models.CharField = Address.neighborhood.field
        self.assertIsInstance(neighborhood_field, models.CharField)
        self.assertFalse(neighborhood_field.null)
        self.assertFalse(neighborhood_field.blank)
        self.assertIsNone(neighborhood_field.db_column)
        self.assertTrue(neighborhood_field.editable)
        self.assertEqual(neighborhood_field.max_length, 255)

        city_field: models.CharField = Address.city.field
        self.assertIsInstance(city_field, models.CharField)
        self.assertFalse(city_field.null)
        self.assertFalse(city_field.blank)
        self.assertIsNone(city_field.db_column)
        self.assertTrue(city_field.editable)
        self.assertEqual(city_field.max_length, 255)

        state_field: models.CharField = Address.state.field
        self.assertIsInstance(state_field, models.CharField)
        self.assertFalse(state_field.null)
        self.assertFalse(state_field.blank)
        self.assertIsNone(state_field.db_column)
        self.assertTrue(state_field.editable)
        self.assertEqual(state_field.max_length, 2)


        zip_code_field: models.CharField = Address.zip_code.field
        self.assertIsInstance(zip_code_field, models.CharField)
        self.assertFalse(zip_code_field.null)
        self.assertFalse(zip_code_field.blank)
        self.assertIsNone(zip_code_field.db_column)
        self.assertTrue(zip_code_field.editable)
        self.assertEqual(zip_code_field.max_length, 9)


class EmailActivationModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        EmailActivation.objects.create(
            user=self.user,
            token=uuid.uuid4(),
        )

    def test_user_label(self):
        email_activation = EmailActivation.objects.get(user=self.user)
        field_label = email_activation._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_token_label(self):
        email_activation = EmailActivation.objects.get(user=self.user)
        field_label = email_activation._meta.get_field('token').verbose_name
        self.assertEqual(field_label, 'token')

    def test_expiration_time_label(self):
        email_activation = EmailActivation.objects.get(user=self.user)
        field_label = email_activation._meta.get_field(
            'expiration_time'
        ).verbose_name
        self.assertEqual(field_label, 'expiration time')

    def test_email_activation_str_method(self):
        email_activation = EmailActivation.objects.get(user=self.user)
        expected_str = f'user: {email_activation.user.email}, token: {email_activation.token}, expira em: {email_activation.expiration_time}'
        self.assertEqual(str(email_activation), expected_str)

    def test_class__meta__(self):
        self.assertEqual(str(EmailActivation._meta), 'placework.emailactivation')

    def test_verbose_name(self):
        self.assertEqual(
            str(EmailActivation._meta.verbose_name), 'Ativação de E-mail'
        )
        self.assertEqual(
            str(EmailActivation._meta.verbose_name_plural),
            'Ativações de E-mail',
        )

    def test_mapping(self):
        table_name = EmailActivation._meta.db_table
        self.assertEqual(table_name, 'placework_emailactivation')

        fields_name = tuple(field.name for field in EmailActivation._meta.fields)
        self.assertEqual(
            fields_name,
            ('id', 'user', 'token', 'expiration_time', 'created_at'),
        )

        user_field: models.ForeignKey = EmailActivation.user.field
        self.assertIsInstance(user_field, models.ForeignKey)
        self.assertFalse(user_field.null)
        self.assertFalse(user_field.blank)
        self.assertIsNone(user_field.db_column)
        self.assertTrue(user_field.editable)

        token_field: models.UUIDField = EmailActivation.token.field
        self.assertIsInstance(token_field, models.UUIDField)
        self.assertFalse(token_field.null)
        self.assertFalse(token_field.blank)
        self.assertIsNone(token_field.db_column)

        expiration_time_field: models.DateTimeField = EmailActivation.expiration_time.field
        self.assertIsInstance(expiration_time_field, models.DateTimeField)
        self.assertFalse(expiration_time_field.null)
        self.assertFalse(expiration_time_field.blank)
        self.assertIsNone(expiration_time_field.db_column)
        self.assertTrue(expiration_time_field.editable)

        created_at_field: models.DateTimeField = EmailActivation.created_at.field
        self.assertIsInstance(created_at_field, models.DateTimeField)
        self.assertFalse(created_at_field.null)
        self.assertTrue(created_at_field.blank)
        self.assertIsNone(created_at_field.db_column)


class PasswordResetCodeModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        expiration_time = timezone.now() + timedelta(hours=1)
        PasswordResetCode.objects.create(
            user=self.user,
            code=uuid.uuid4(),
            expiration_time=expiration_time,
        )

    def test_user_label(self):
        password_reset_code = PasswordResetCode.objects.get(user=self.user)
        field_label = password_reset_code._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_code_label(self):
        password_reset_code = PasswordResetCode.objects.get(user=self.user)
        field_label = password_reset_code._meta.get_field('code').verbose_name
        self.assertEqual(field_label, 'code')

    def test_expiration_time_label(self):
        password_reset_code = PasswordResetCode.objects.get(user=self.user)
        field_label = password_reset_code._meta.get_field(
            'expiration_time'
        ).verbose_name
        self.assertEqual(field_label, 'expiration time')

    def test_password_reset_code_str_method(self):
        password_reset_code = PasswordResetCode.objects.get(user=self.user)
        expected_str = f'user: {password_reset_code.user.email}, code: {password_reset_code.code}, expira em: {password_reset_code.expiration_time}'
        self.assertEqual(str(password_reset_code), expected_str)

    def test_class__meta__(self):
        self.assertEqual(
            str(PasswordResetCode._meta), 'placework.passwordresetcode'
        )

    def test_verbose_name(self):
        self.assertEqual(
            str(PasswordResetCode._meta.verbose_name), 'Código de Redefinição de Senha'
        )
        self.assertEqual(
            str(PasswordResetCode._meta.verbose_name_plural),
            'Códigos de Redefinição de Senha',
        )

    def test_mapping(self):
        table_name = PasswordResetCode._meta.db_table
        self.assertEqual(table_name, 'placework_passwordresetcode')

        fields_name = tuple(field.name for field in PasswordResetCode._meta.fields)
        self.assertEqual(
            fields_name,
            ('id', 'user', 'code', 'expiration_time', 'created_at'),
        )

        user_field: models.ForeignKey = PasswordResetCode.user.field
        self.assertIsInstance(user_field, models.ForeignKey)
        self.assertFalse(user_field.null)
        self.assertFalse(user_field.blank)
        self.assertIsNone(user_field.db_column)
        self.assertTrue(user_field.editable)

        code_field: models.UUIDField = PasswordResetCode.code.field
        self.assertIsInstance(code_field, models.UUIDField)
        self.assertFalse(code_field.null)
        self.assertFalse(code_field.blank)
        self.assertIsNone(code_field.db_column)

        expiration_time_field: models.DateTimeField = PasswordResetCode.expiration_time.field
        self.assertIsInstance(expiration_time_field, models.DateTimeField)
        self.assertFalse(expiration_time_field.null)
        self.assertFalse(expiration_time_field.blank)
        self.assertIsNone(expiration_time_field.db_column)
        self.assertTrue(expiration_time_field.editable)

        created_at_field: models.DateTimeField = PasswordResetCode.created_at.field
        self.assertIsInstance(created_at_field, models.DateTimeField)
        self.assertFalse(created_at_field.null)
        self.assertTrue(created_at_field.blank)
        self.assertIsNone(created_at_field.db_column)


class PasswordHistoryModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        PasswordHistory.objects.create(
            user=self.user,
            hashed_password='testhashedpassword',
        )

    def test_user_label(self):
        password_history = PasswordHistory.objects.get(user=self.user)
        field_label = password_history._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_hashed_password_label(self):
        password_history = PasswordHistory.objects.get(user=self.user)
        field_label = password_history._meta.get_field(
            'hashed_password'
        ).verbose_name
        self.assertEqual(field_label, 'hashed password')

    def test_password_history_str_method(self):
        password_history = PasswordHistory.objects.get(user=self.user)
        expected_str = f'user: {password_history.user.email}, pass: {password_history.hashed_password}'
        self.assertEqual(str(password_history), expected_str)

    def test_class__meta__(self):
        self.assertEqual(
            str(PasswordHistory._meta), 'placework.passwordhistory'
        )

    def test_verbose_name(self):
        self.assertEqual(
            str(PasswordHistory._meta.verbose_name), 'Histórico de Senhas'
        )
        self.assertEqual(
            str(PasswordHistory._meta.verbose_name_plural),
            'Históricos de Senhas',
        )

    def test_mapping(self):
        table_name = PasswordHistory._meta.db_table
        self.assertEqual(table_name, 'placework_passwordhistory')

        fields_name = tuple(field.name for field in PasswordHistory._meta.fields)
        self.assertEqual(
            fields_name,
            ('id', 'user', 'hashed_password'),
        )

        user_field: models.ForeignKey = PasswordHistory.user.field
        self.assertIsInstance(user_field, models.ForeignKey)
        self.assertFalse(user_field.null)
        self.assertFalse(user_field.blank)
        self.assertIsNone(user_field.db_column)
        self.assertTrue(user_field.editable)

        hashed_password_field: models.CharField = PasswordHistory.hashed_password.field
        self.assertIsInstance(hashed_password_field, models.CharField)
        self.assertFalse(hashed_password_field.null)
        self.assertFalse(hashed_password_field.blank)
        self.assertIsNone(hashed_password_field.db_column)
        self.assertTrue(hashed_password_field.editable)
        self.assertEqual(hashed_password_field.max_length, 128)


