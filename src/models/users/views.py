from flask import Blueprint, request, session, redirect, url_for, render_template, flash
from src.models.users.user import User
from src.models.users.errors import UserNotExistsError
import src.models.users.errors as UserErrors
from src.models.users.decorators import requires_login
from src.common.flask_redirect import redirect_url

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods=["GET","POST"])
def login_user():
    if request.method == "POST":
        # Check if login is valid

        email = request.form["userForm-email"]
        password = request.form["userForm-pass"]

        try:
            if User.is_login_valid(email, password):
                user = User.find_by_email(email)
                session["email"] = user.email
                session["username"] = user.username
                return redirect(redirect_url()) 

        except UserErrors.UserError as e:
            flash(e.message, 'login')

    return redirect(redirect_url()) 


@user_blueprint.route('/logout')
def logout_user():
    session["email"] = None
    session["username"] = None
    return redirect(url_for("home"))


@user_blueprint.route('/register', methods=["GET","POST"])
def register_user():
    if request.method == "POST":
        # Check if login is valid
        email = request.form["userRegisterForm-email"]
        password = request.form["userRegisterForm-pass"]
        username = request.form["userRegisterForm-name"]
        try:
            if User.register_user(email, password, username):
                session["email"] = email
                session["username"] = username
                return redirect(redirect_url())
        except UserErrors.UserError as e:
            flash(e.message, 'register')

    return redirect(redirect_url())     


# @user_blueprint.route('/alerts')
# @requires_login
# def user_alerts():
#     return redirect(url_for("stores.index"))



# @user_blueprint.route('/check_alerts/<string:user_id>')
# def check_user_alerts(user_id):
#     pass
