#!/usr/bin/env python3
""" Main module to interact. """
from auth import Auth
import requests


def register_user(email: str, password: str) -> None:
    """ Register a new user."""
    pass


def log_in_wrong_password(email: str, password: str) -> None:
    """ Log in with the specified email and password."""
    pass


def profile_unlogged() -> None:
    """ assert correct response to the profile."""
    pass


def log_in(email: str, password: str) -> str:
    """ Log in with the specified email and password."""
    return None


def profile_logged(session_id: str) -> None:
    """ Access the profile page."""
    pass


def log_out(session_id: str) -> None:
    """ Log out using the specified session id."""
    pass


def reset_password_token(email: str) -> str:
    """ Generate a reset password token for the specified email0."""
    return None


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Update the password for the specified email using the reset token.
    """
    pass


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://127.0.0.1:5000"

if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
