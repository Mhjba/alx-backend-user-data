#!/usr/bin/env python3
"""add an expiration date to a Session ID"""
from models.user import User
from os import getenv
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta



class SessionExpAuth(SessionAuth):
    """Session Expiration Class"""

    def __init__(self):
        """Constructor Method"""
        SESSION_DURATION = getenv('SESSION_DURATION')

        try:
            sess_duration = int(SESSION_DURATION)
        except Exception:
            sess_duration = 0

        self.sess_duration = sess_duration

    def create_session(self, user_id=None):
        """Creation session with expiration"""

        sess_id = super().create_session(user_id)

        if sess_id is None:
            return None

        sess_dic = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        self.user_id_by_session_id[sess_id] = sess_dic

        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """ gets user_id from session_id """

        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None

        sess_dic = self.user_id_by_session_id.get(session_id)

        if sess_dic is None:
            return None

        if self.sess_duration <= 0:
            return sess_dic.get('user_id')

        created_at = sess_dic.get('created_at')

        if created_at is None:
            return None

        expired_time = created_at + timedelta(seconds=self.session_duration)

        if expired_time < datetime.now():
            return None

        return sess_dic.get('user_id')
