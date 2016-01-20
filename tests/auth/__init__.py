import unittest


from argux_server.auth import register_auth_functions

def valid_func(username, password):
    return

def too_few_args(aaa):
    return

def too_many_args(username, password, something_else):
    return

def missing_username(password, something_else):
    return

def missing_password(username, something_else):
    return

class AuthenticationTests(unittest.TestCase):

    def test_register_auth_missing_username(self):
        """Test register_auth_func error with missing username argument.

        register_auth_func(name, func) requires a function
        with the following prototype auth(username, password).
        It raises a ValueError if a function does not follow this
        format.

        This Test validates the error-message when the function
        is missing a 'username' argument. 
        """
        with self.assertRaises(ValueError) as cm:
            register_auth_functions(
                'missing_username',
                missing_username,
                missing_username)

        exception = cm.exception
        self.assertEqual(
            format(exception),
            "Function has no 'username' argument")

    def test_register_auth_missing_password(self):
        """Test register_auth_func error with missing password argument.

        register_auth_func(name, func) requires a function
        with the following prototype auth(username, password).
        It raises a ValueError if a function does not follow this
        format.

        This Test validates the error-message when the function
        is missing a 'password' argument. 
        """
        with self.assertRaises(ValueError) as cm:
            register_auth_functions(
                'missing_password',
                missing_password,
                missing_password)

        exception = cm.exception
        self.assertEqual(
            format(exception),
            "Function has no 'password' argument")

    def test_register_auth_too_many_args(self):
        """Test register_auth_func error with too many arguments.

        register_auth_func(name, func) requires a function
        with the following prototype auth(username, password).
        It raises a ValueError if a function does not follow this
        format.

        This Test validates the error-message when the function does
        not have the right number of arguments.
        """
        with self.assertRaises(ValueError) as cm:
            register_auth_functions(
                'too_many_args',
                too_many_args,
                too_many_args)

        exception = cm.exception
        self.assertEqual(
            format(exception),
            "Function has 3 arguments, expected 2")

    def test_register_auth_too_few_args(self):
        """Test register_auth_func error with too few arguments.

        register_auth_func(name, func) requires a function
        with the following prototype auth(username, password).
        It raises a ValueError if a function does not follow this
        format.

        This Test validates the error-message when the function does
        not have the right number of arguments.
        """
        with self.assertRaises(ValueError) as cm:
            register_auth_functions(
                'too_few_args',
                too_few_args,
                too_few_args)

        exception = cm.exception
        self.assertEqual(
            format(exception),
            "Function has 1 arguments, expected 2")

    def test_register_valid_func(self):
        """Test behaviour if a valid auth_func is registered."""

        register_auth_functions('valid_func', valid_func, valid_func)

    def test_register_duplicates(self):
        """Test register_auth_func error with duplicate names.

        register_auth_func(name, func) requires a function
        with the following prototype auth(username, password)
        and a name argument.
.
        It raises a ValueError if a function with a simmilar
        name is already registered.

        This Test validates the error-message when a duplicate
        name already exists.
        """

        register_auth_functions('duplicate', valid_func, valid_func)

        with self.assertRaises(ValueError) as cm:
            register_auth_functions('duplicate', valid_func, valid_func)

        exception = cm.exception
        self.assertEqual(
            format(exception),
            "Function name 'duplicate' already exists")
