#!/usr/bin/env python3
""" Module of User Authentication """
from os import getenv
from flask import jsonify, abort, request
from api.v1.views import app_views
from typing import TypeVar, List


class Auth:
    """Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth
        """
        if not path or not excluded_paths or excluded_paths == []:
            return True

        if not path.endswith('/'):
            path = path + '/'

        for auth in excluded_paths:
            if auth == path or path.startswith(auth.split('*')[0]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization heade
        """
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user
        """
        return None

    def session_cookie(self, request=None):
        """session cookie"""
        if request is None:
            return None
        _my_session_id = getenv("SESSION_NAME")
        return request.cookies.get(_my_session_id)
