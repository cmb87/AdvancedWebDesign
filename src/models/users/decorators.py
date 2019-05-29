from functools import wraps
from flask import redirect, session,url_for, request
import src.config as config

def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session["email"] is None:
            # If user is not logged in, he will be redirected to the login page.
            # Upon login, we are jumping back to the current side with the
            # help of the next=request.path() flask command
            return redirect(url_for('users.login_user', next=request.path))
        return func(*args, **kwargs)
    return decorated_function


def is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session["email"] not in config.ADMINS:
            return redirect(url_for('home'))
        return func(*args, **kwargs)
    return decorated_function