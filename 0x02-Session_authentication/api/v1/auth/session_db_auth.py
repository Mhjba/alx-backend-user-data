#!/usr/bin/env python3
""" Module of Session in Database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """authentication class"""

    def create_session(self, user_id=None):
        """Creation session database"""
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        kwargs = {'user_id': user_id, 'session_id': session_id}
        user_sess = UserSession(**kwargs)
        user_sess.save()
        UserSession.save_to_file()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """User ID for Session ID Database"""
        if session_id is None:
            return None

        UserSession.load_from_file()
        user_sess = UserSession.search({
            'session_id': session_id
        })

        if not user_sess:
            return None

        user_sess = user_sess[0]

        expired_time = user_sess.created_at + \
            timedelta(seconds=self.session_duration)

        if expired_time < datetime.utcnow():
            return None

        return user_sess.user_id

    def destroy_session(self, request=None):
        """Remove Session from Database"""
        if request is None:
            return False

        sess_id = self.session_cookie(request)
        if sess_id is None:
            return False

        user_id = self.user_id_for_session_id(sess_id)

        if not user_id:
            return False

        user_sess = UserSession.search({
            'session_id': sess_id
        })

        if not user_sess:
            return False

        user_sess = user_sess[0]

        try:
            user_sess.remove()
            UserSession.save_to_file()
        except Exception:
            return False

        return True
