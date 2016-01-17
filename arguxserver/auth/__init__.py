"""Authentication Module."""

import inspect

_auth_methods = {}
_passwd_methods = {}

def _validate_function(func):
    argspec = inspect.getargspec(func)
    if len(argspec.args) != 2:
        raise ValueError(
            "Function has {} arguments, expected 2"\
            .format(len(argspec.args)))
    if not "username" in argspec.args:
        raise ValueError("Function has no 'username' argument")
    if not "password" in argspec.args:
        raise ValueError("Function has no 'password' argument")

    return

def register_auth_functions(name, auth_func, passwd_func):
    """Register auth and passwd func."""
    _validate_function(auth_func)
    _validate_function(passwd_func)

    if name in _auth_methods:
        raise ValueError(
            "Function name '{}' already exists"\
            .format(name))

    _auth_methods[name] = auth_func
    _passwd_methods[name] = passwd_func
