"""BCRYPT Authentication Module."""

import bcrypt

# Number of hashing rounds
WORK_FACTOR = 15

def gen_hash(password):
    """Function for generating a password-hash using bcrypt."""
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(WORK_FACTOR))
    return hashed

def validate(password, hashed):
    """Function for validating the password-hash using bcrypt."""
    if bcrypt.hashpw(password, hashed) == hashed:
        return True
    else:
        return False
