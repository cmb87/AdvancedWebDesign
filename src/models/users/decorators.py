from functools import wraps
from flask import redirect, session,url_for, request, flash
import src.config as config
from src.common.flask_redirect import redirect_url


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session["email"] is None:
            # If user is not logged in, he will be redirected to the login page.
            # Upon login, we are jumping back to the current side with the
            # help of the next=request.path() flask command
            flash('You need to be logged in to use this feature!', 'login')
            return redirect(redirect_url()) 
        return func(*args, **kwargs)
    return decorated_function


def is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session["email"] not in config.ADMINS:
            flash('You need to be an Admin to use this feature!', 'login')
            return redirect(redirect_url()) 
        return func(*args, **kwargs)
    return decorated_function