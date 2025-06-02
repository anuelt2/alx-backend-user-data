#!/usr/bin/env python3
"""Auth module"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Takes password and returns salted hash as byte string"""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Create user with a unique email and a password, save to database"""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {user.email} already exists.")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(
                    email=email,
                    hashed_password=hashed_password
                    )
            return user
