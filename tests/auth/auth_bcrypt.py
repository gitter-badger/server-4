import unittest

import bcrypt

from argux_server.auth.auth_bcrypt import (
    gen_hash,
    validate
)


class AuthBcryptTests(unittest.TestCase):

    def test_gen_hash(self):
        """Test gen_hash generated hash with bcrypt.hashpw."""
        hashed = gen_hash('test_password')

        self.assertEqual(
            bcrypt.hashpw(
                'test_password'.encode('utf-8'),
                hashed),
            hashed)

    def test_validate(self):
        """Test validate function against generated bcrypt hash."""
        hashed = bcrypt.hashpw(
            'test_password'.encode('utf-8'),
            bcrypt.gensalt(15))

        self.assertTrue(validate('test_password', hashed))

        self.assertFalse(validate('test_password_no', hashed))
