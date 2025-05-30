#!/usr/bin/env python3
""" Module for SessionDBAuth class
"""

from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class
    """

    def create_session(self, user_id=None):
        """ Creates and stores a new instance of UserSession,
        returns Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return user_session.session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns the User ID by requesting UserSession in database
        based on session_id
        """
        if session_id is None:
            return None

        sessions = UserSession.search({"session_id": session_id})
        if not sessions:
            return None

        user_session = sessions[0]

        if self.session_duration <= 0:
            return user_session.user_id

        if not user_session.created_at:
            return None

        expiration_time = user_session.created_at + \
            timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """ Destroys the UserSession based on Session ID from  request cookie
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return False

        user_session = sessions[0]
        user_session.remove()
        UserSession.save_to_file()
        return True
