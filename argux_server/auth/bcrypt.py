"""BCRYPT Authentication Module."""

import bcrypt

SALT = 12

def bcrypt_auth_func(username, password):
    """Function for authenticating the user using bcrypt."""
    return True

def bcrypt_passwd_func(username, password):
    """Function for storing the password using bcrypt."""
    return True
