import unittest
from unittest.mock import MagicMock, patch

import bcrypt
from django.test import TestCase

from placework.utils import generate_password, hash_password


class HashPasswordTestCase(unittest.TestCase):
    @patch('bcrypt.gensalt', MagicMock(return_value=b'salt123'))
    @patch('bcrypt.hashpw', MagicMock(return_value=b'hashed_password'))
    def test_hash_password(self):
        password = 'MinhaSenhaSegura123'
        hashed_password = hash_password(password)
        bcrypt.gensalt.assert_called_once_with()
        bcrypt.hashpw.assert_called_once_with(
            password.encode('utf-8'), b'salt123'
        )
        self.assertEqual(hashed_password, 'hashed_password')


class TestGeneratePassword(TestCase):
    def test_generate_password(self):
        password = generate_password()

        self.assertIsInstance(password, str)
        self.assertEqual(len(password), 8)

        # Verifique se a senha é composta apenas de caracteres hexadecimais (0-9, a-f)
        valid_characters = set('0123456789abcdef')
        for char in password:
            self.assertIn(char, valid_characters)
