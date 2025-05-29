#!/usr/bin/env python3
""" Module for Auth class to manage API authentication
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ Template for authentication system
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is required for a given path
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        if not path.endswith("/"):
            path = path + "/"

        wildcard_paths = [wc_path for wc_path in excluded_paths
                          if wc_path.endswith("*")]
        if len(wildcard_paths) > 0:
            for wc_path in wildcard_paths:
                if path.startswith(wc_path[:-1]):
                    return False

        if path not in excluded_paths:
            return True

        return False

    def authorization_header(self, request=None) -> str:
        """ Retrieves authorization header from Flask request object
        """
        if request is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves current user from Flask request object
        """
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request
        """
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        return request.cookies.get(session_name)
