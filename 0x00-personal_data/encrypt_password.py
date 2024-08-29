#!/usr/bin/env python3
"""
encrypting your password
"""

import bcrypt


def hash_password(password: str) -> str:
    pass_bytes = password.encode('utf-8')
    return bcrypt.hashpw(pass_bytes, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
