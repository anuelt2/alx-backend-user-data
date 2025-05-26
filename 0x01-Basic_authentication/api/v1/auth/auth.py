#!/usr/bin/env python3
""" Module for Auth class to manage API authentication
"""
from flask import request
from typing import List, TypeVar


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
