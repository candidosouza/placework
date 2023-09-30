from unittest.mock import Mock

from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import TestCase

from placework.admin import UserAdmin


class UserAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.user_admin = UserAdmin(User, self.site)

    def test_should_a_model_admin_instance(self):
        self.assertIsInstance(self.user_admin, ModelAdmin)

    def test_should_the_model_attr_be_a_user_class(self):
        self.assertEqual(self.user_admin.model, User)

    def test_list_display(self):
        expected_fields = ('name', 'email', 'accout_type', 'cpf_cnpj')
        self.assertEqual(UserAdmin.list_display, expected_fields)

    def test_search_fields(self):
        expected_fields = (
            'first_name',
            'last_name',
            'email',
            'user_profile__cpf',
            'user_profile__cnpj',
            'user_profile__company_name',
        )
        self.assertEqual(UserAdmin.search_fields, expected_fields)

    def test_list_filter(self):
        expected_fields = (
            'user_profile__account_type',
            'user_profile__is_active',
        )
        self.assertEqual(UserAdmin.list_filter, expected_fields)
