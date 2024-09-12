#!/usr/bin/env python3
"""
file to handle password encryption
"""
import bcrypt
from user import User
from db import DB
from sqlalchemy.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
    hash a password using bcypt
    """
    encoded_pwd = password.encode('utf-8')
    return bcrypt.hashpw(encoded_pwd, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        register or add a user to our datbase
        """
        if not email or not password:
            raise ValueError("provide both email and password")
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hash_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hash_pwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        validate user credentials before logging
        in
        """
        user = self._db.find_user_by(email=email)
        encode_pwd = password.encode('utf-8')
        try:
            if user and bcrypt.checkpw(encode_pwd, user.hashed_password):
                return True
        except NoResultFound:
            return False
        except Exception as e:
            return False
        return False

    def _generate_uuid() -> str:
        """
        generate a unique id
        """
        return str(uuid.uuid4())
