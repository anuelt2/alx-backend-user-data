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
        return False

    def authorization_header(self, request=None) -> str:
        """ Retrieves authorization header from Flask request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves current user from Flask request object
        """
        return None
