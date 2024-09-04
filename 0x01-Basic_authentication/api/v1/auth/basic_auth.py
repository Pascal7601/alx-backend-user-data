#!/usr/bin/env python3
"""

"""
from .auth import Auth
import base64
from typing import Tuple, Optional


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
        
