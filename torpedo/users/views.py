from flask import render_template, request

from passlib.hash import pbkdf2_sha256

from torpedo import torpedo_app

from torpedo.users.models import User
from torpedo.users.forms import UserLoginForm, UserSignupForm


@torpedo_app.route('/login', methods=["GET", "POST"])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        # Find user with given email
        user = User.objects(email=form.data["email"])

        # Generate hash for password
        password_hash = pbkdf2_sha256.hash(form.data["password"])

        # Check if login is valid
    else:
        return render_template("users/login.html", form=form)


@torpedo_app.route("/signup", methods=["GET", "POST"])
def signup():
    form = UserSignupForm()
    if form.validate_on_submit():
        pass
    else:
        return render_template("users/signup.html", form=form)
