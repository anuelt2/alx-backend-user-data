#!/usr/bin/env python3
""" Module for SessionExpAuth class
"""

from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ Implement expiration date for a Session ID
    """

    def __init__(self):
        """ Initialize SessionExpAuth instance
        """
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION", "0"))
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Creates a session id and store time it was created
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dictionary = {
                "user_id": user_id,
                "created_at": datetime.now()
                }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID based on a Session ID, and checks expiration
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get("user_id")

        created_at = session_dict.get("created_at")
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return session_dict.get("user_id")
