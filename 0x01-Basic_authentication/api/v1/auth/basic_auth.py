#!/usr/bin/env python3
""" Module for BasicAuth class to handle `basic_auth` `AUTH_TYPE`
"""
import base64
from api.v1.auth.auth import Auth


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
