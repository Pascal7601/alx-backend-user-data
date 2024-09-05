#!/usr/bin/env python3
"""

"""
from .auth import Auth
import base64
from typing import Tuple, Optional, TypeVar
from models.user import User

class BasicAuth(Auth):
    """
    Extracts the Base64 part from the Authorization
    header for Basic Authentication
    """
    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
        if authorization_header is None:
            return None
        
        if not isinstance(authorization_header, str):
            return None
        
        if not authorization_header.startswith('Basic '):
            return None
        
        return authorization_header[6:]
    

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
            ) -> str:
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return  None
        
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            
            decoded_str = decoded_bytes.decode('utf-8')

            return decoded_str
        except:
            return None
        
    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
            ) -> Tuple[Optional[str], Optional[str]]:
        """
        
        """
        if decoded_base64_authorization_header is None:
            return None, None
        
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        
        if ':' not in decoded_base64_authorization_header:
            return None, None
        
        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)
    

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """
        
        """
        if user_email is None or user_pwd is None:
            return None
        user = User()
        user_list = user.search({"email": user_email})
        if len(user_list) == 0:
            return None
        user = user_list[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user
        
    
    def current_user(self, request=None) -> User:
        """
        obtains details of current user
        """
        if request is None:
            return None
        
        auth_header = self.extract_base64_authorization_header(self.authorization_header(request))
        decoded_auth = self.decode_base64_authorization_header(auth_header)
        email, password = self.extract_user_credentials(decoded_auth)
        return self.user_object_from_credentials(email, password)
