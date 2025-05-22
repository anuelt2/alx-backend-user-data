#!/usr/bin/env python3
"""encrypt_password module"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Takes a password and returns a salted, hashed password as byte string"""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates password against hashed"""
    return bcrypt.checkpw(password.encode(), hashed_password)
