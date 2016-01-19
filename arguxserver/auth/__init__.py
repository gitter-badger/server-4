"""Authentication Module."""

import inspect

__AUTH_METHODS = {}
__PASSWD_METHODS = {}

def __validate_function(func):
    sig = inspect.signature(func)
    if len(sig.parameters) != 2:
        raise ValueError(
            "Function has {} arguments, expected 2"\
            .format(len(sig.parameters)))
    if "username" not in sig.parameters:
        raise ValueError("Function has no 'username' argument")
    if "password" not in sig.parameters:
        raise ValueError("Function has no 'password' argument")

    return

def register_auth_functions(name, auth_func, passwd_func):
    """Register auth and passwd func."""
    __validate_function(auth_func)
    __validate_function(passwd_func)

    if name in __AUTH_METHODS:
        raise ValueError(
            "Function name '{}' already exists"\
            .format(name))

    __AUTH_METHODS[name] = auth_func
    __PASSWD_METHODS[name] = passwd_func
