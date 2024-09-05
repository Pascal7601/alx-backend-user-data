#!/usr/bin/env python3
"""
handling authorization
"""

from flask import request
from typing import List
from typing import TypeVar
from os import getenv
from dotenv import load_dotenv


load_dotenv()

class Auth:
    """
    Base class for handling authorization
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        determines the paths to not authenticate
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Normalize the path
        normal_path = path if path.endswith('/') else path + '/'

        # Check if the path is in the list of excluded paths
        if normal_path in excluded_paths:
            return False

        return True
        
    
    def authorization_header(self, request=None) -> str:
        """
        gets the token from the authorization header
        """
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
        return auth_header
    
    def current_user(self, request=None) -> TypeVar('User'):
        """
        
        """
        return None
    

    def session_cookie(self, request=None):
        """
        return a cookie value from a request
        """
        if request is None:
            return None
        my_session = getenv('SESSION', '_my_session_id')
        return request.cookies.get(my_session)

