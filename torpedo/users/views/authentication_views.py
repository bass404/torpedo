from flask import render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user

from torpedo import torpedo_app, login_manager

from torpedo.users.models import User, hash_password, UserRole
from torpedo.users.forms import UserLoginForm, UserSignupForm


@login_manager.user_loader
def load_user(user_id):
    user = User.objects(id=user_id)
    if not user:
        return None
    return user[0]


@torpedo_app.route('/login', methods=["GET", "POST"])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        # Find user with given email
        user = User.objects(email=form.data["email"])

        if not user:
            flash("User not found")
            return redirect(url_for('login'))
        else:
            user = user[0]

        if user.check_password(form.data["password"]):
            # Login user
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Invalid login")
            return redirect(url_for("login"))
    else:
        return render_template("users/login.html", form=form)


@torpedo_app.route("/signup", methods=["GET", "POST"])
def signup():
    form = UserSignupForm()

    if form.validate_on_submit():
        # Check if password and confirm_password field match
        password = form.data["password"]
        confirm_password = form.data["confirm_password"]

        if password != confirm_password:
            flash("Passwords doesn't match")
            return redirect(url_for('signup'))

        # Generate password hash
        password_hash = hash_password(form.data["password"])

        # Create user model with email and password
        user = User(email=form.data["email"], password=password_hash)

        # Add other properties to User model
        user.first_name = form.data["first_name"]
        user.last_name = form.data["last_name"]
        user.save()

        # Create a role for user
        user_role = UserRole(user_id=user.id)
        user_role.save()

        # Login user and redirect to index page
        flash("User created")
        return redirect(url_for('signup'))
    else:
        return render_template("users/signup.html", form=form)


@torpedo_app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
