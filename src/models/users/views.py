from flask import Blueprint, request, session, redirect, url_for, render_template
from src.models.users.user import User
from src.models.users.errors import UserNotExistsError
import src.models.users.errors as UserErrors
from src.models.users.decorators import requires_login

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods=["GET","POST"])
def login_user():
    if request.method == "POST":
        # Check if login is valid
        email = request.form["email"]
        password = request.form["hashed"]
        try:
            if User.is_login_valid(email, password):
                session["email"] = email
                return redirect(url_for(".user_alerts"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/login.html") # Send the user an error if login was invalid


@user_blueprint.route('/register', methods=["GET","POST"])
def register_user():
    if request.method == "POST":
        # Check if login is valid
        email = request.form["email"]
        password = request.form["hashed"]
        try:
            if User.register_user(email, password):
                session["email"] = email
                return redirect(url_for("stores.index"))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/register.html") # Send the user an error if login was invalid


@user_blueprint.route('/alerts')
@requires_login
def user_alerts():
    return redirect(url_for("stores.index"))


@user_blueprint.route('/logout')
def logout_user():
    session["email"] = None
    return redirect(url_for('home'))

@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts(user_id):
    pass
