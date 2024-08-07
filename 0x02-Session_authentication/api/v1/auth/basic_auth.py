#!/usr/bin/env python3
""" Module of User Authentication """
from .auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract base64 authorization header"""
        if (authorization_header is None or
            type(authorization_header) is not str or
                not authorization_header.startswith("Basic ")):
            return None
        return (authorization_header[6:])

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decode base64 authorization header"""
        if (base64_authorization_header is None or
                type(base64_authorization_header) is not str):
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode()
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract user credentials"""
        if (decoded_base64_authorization_header is None or
            type(decoded_base64_authorization_header) is not str or
                ":" not in decoded_base64_authorization_header):
            return None, None
        return decoded_base64_authorization_header.split(':', 1)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """user object from credentials"""
        if (user_email is None or type(user_email) is not str or
                type(user_pwd) is not str):
            return None
        if (User.search({'email': user_email})):
            user = User.search({'email': user_email})
            for us in user:
                if us.is_valid_password(user_pwd):
                    return us
                return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user"""
        auth_header = self.authorization_header(request)
        auth_b64 = self.extract_base64_authorization_header(auth_header)
        auth_decoded = self.decode_base64_authorization_header(auth_b64)
        auth_data = self.extract_user_credentials(auth_decoded)
        return self.user_object_from_credentials(*auth_data)
