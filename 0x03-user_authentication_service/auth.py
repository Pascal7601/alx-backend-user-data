#!/usr/bin/env python3
"""
file to handle password encryption
"""
import bcrypt
from user import User
from db import DB
from sqlalchemy.exc import NoResultFound
import uuid
from typing import Optional


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
        Validate the login credentials.
        """
        try:
            # Try to find the user by email
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            # If no user is found, return False
            return False

        # Check if the password matches the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
            return True
        return False

    def _generate_uuid(self) -> str:
        """
        generate a unique id
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """
        generate a sessiion id
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: Optional[str]) -> Optional[User]:
        """
        Retrieve a user based on the session ID.
        """
        if session_id is None:
            return None

        try:
            # Find user by session_id
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            # If no user is found, return None
            return None

        return user

    def destroy_session(self, user_id: int):
        """
        destroy a suer session
        """
        self._db.update_user(user_id, session_id=None)
        return None
