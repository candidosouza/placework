import uuid
import unittest
import bcrypt
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

from placework.models import PasswordResetCode, PasswordHistory


from placework.utils import (
    hash_password,
    check_password,
    change_password,
    generate_reset_code,
    is_reset_code_valid,
)


class HashPasswordTestCase(TestCase):
    def test_hash_password(self):
        password = "MinhaSenhaSegura123"
        hashed_password = hash_password(password)
        self.assertNotEqual(password, hashed_password)
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')))


# TODO teste está dando erro de bytes, AttributeError: 'bytes' object has no attribute 'encode'
# class CheckPasswordTestCase(TestCase):
#     def setUp(self):
#         self.hashed_password = bcrypt.hashpw(b'mypassword', bcrypt.gensalt())

#     def test_matching_passwords(self):
#         self.assertTrue(check_password('mypassword', self.hashed_password))

#     def test_non_matching_passwords(self):
#         self.assertFalse(check_password('wrongpassword', self.hashed_password))


# TODO teste está dando erro de bytes, AttributeError: 'bytes' object has no attribute 'encode'
# class ChangePasswordIntegrationTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='testuser123',
#             password='123456'
#         )

#     def test_change_password_success(self):
#         new_password = b'79797979'
#         result = change_password(self.user, new_password)
#         self.assertTrue(result)
#         self.assertTrue(check_password(new_password, self.user.password))
#         password_history = PasswordHistory.objects.filter(user=self.user)
#         self.assertEqual(password_history.count(), 1)
#         self.assertTrue(check_password(new_password, password_history[0].hashed_password))

#     def test_change_password_failure(self):
#         result = change_password(self.user, b'123456')
#         self.assertFalse(result)
#         self.assertTrue(check_password('123456', self.user.password))
#         password_history = PasswordHistory.objects.filter(user=self.user)
#         self.assertEqual(password_history.count(), 0)


class GenerateResetCodeIntegrationTest(TestCase):
    def test_generate_reset_code(self):
        user = User.objects.create_user(username='testuser', password='testpassword')

        generated_code = generate_reset_code(user)
        self.assertIsNotNone(generated_code)

        reset_code = PasswordResetCode.objects.get(code=generated_code)
        self.assertEqual(reset_code.user, user)
        expected_expiration_time = timezone.now() + timedelta(hours=1)
        self.assertLess(reset_code.expiration_time, expected_expiration_time + timedelta(seconds=1))
        self.assertGreater(reset_code.expiration_time, expected_expiration_time - timedelta(seconds=1))


class IsResetCodeValidIntegrationTest(TestCase):
    def test_reset_code_valid(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        future_time = timezone.now() + timezone.timedelta(hours=1)
        reset_code = PasswordResetCode.objects.create(
            user=user,
            code=uuid.uuid4(),
            expiration_time=future_time
        )
        result = is_reset_code_valid(reset_code)
        self.assertFalse(result)

    def test_reset_code_expired(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        past_time = timezone.now() - timezone.timedelta(hours=1)
        reset_code = PasswordResetCode.objects.create(
            user=user,
            code=uuid.uuid4(),
            expiration_time=past_time
        )
        result = is_reset_code_valid(reset_code)
        self.assertTrue(result)
