#!/usr/bin/env python3
"""
file to handle password encryption
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    hash a password using bcypt
    """
    encoded_pwd = password.encode('utf-8')
    return bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())
