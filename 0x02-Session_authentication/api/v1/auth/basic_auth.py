#!/usr/bin/env python3
""" Module for BasicAuth class to handle `basic_auth` `AUTH_TYPE`
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic auth authentication system
    """
    def extract_base64_authorization_header(self, authorization_header: str
                                            ) -> str:
        """
        Returns the Base64 part of the Authorization header for a
        Basic Authentication
        """
        basic_prefix = "Basic "
        if authorization_header is None \
                or not isinstance(authorization_header, str) \
                or not authorization_header.startswith(basic_prefix):
            return None
        return authorization_header[len(basic_prefix):]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """ Returns decoded value of a Base64 string
        """
        if base64_authorization_header is None \
                or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """ Returns the user email and passweord from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(":", 1)
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """ Returns the User instance based on email and password
        """
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
        except KeyError:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Auth and retrieves the User instance for a request
        """
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        base64_auth_header = self.extract_base64_authorization_header(
                auth_header
                )
        if not base64_auth_header:
            return None

        decoded_base64_auth_header = self.decode_base64_authorization_header(
                base64_auth_header
                )
        if not decoded_base64_auth_header:
            return None

        user_email, user_pwd = self.extract_user_credentials(
                decoded_base64_auth_header
                )
        if not user_email or not user_pwd:
            return None

        current_user = self.user_object_from_credentials(user_email, user_pwd)
        if not current_user:
            return None

        return current_user
