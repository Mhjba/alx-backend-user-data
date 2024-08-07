#!/usr/bin/env python3
""" Module of session auth views
"""
from .auth import Auth
from typing import TypeVar
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Basic User Auth"""

    # def __init__(self) -> None:
    #     super().__init__()

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None

        sessionID = str(uuid4())
        # subscript Notatation
        self.user_id_by_session_id[sessionID] = user_id
        return sessionID

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """instance method that returns a User ID based on a Session ID:"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """method (overload) that returns a User
            instance based on a cookie value
        """
        sessionID = self.session_cookie(request)
        userID = self.user_id_for_session_id(sessionID)
        return User.get(userID)

    def destroy_session(self, request=None):
        """deletes the user session / logout"""
        if not request:
            return False
        sessionID = self.session_cookie(request)
        if not sessionID or not self.user_id_for_session_id(sessionID):
            return False
        self.user_id_by_session_id.pop(sessionID)
        return True
