import urllib

from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import login_user, login_required, logout_user, current_user

from torpedo import torpedo_app, login_manager

from torpedo.users.models import User, hash_password, UserAddress
from torpedo.users.forms import UserLoginForm, UserSignupForm, UserAddressForm


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


@torpedo_app.route("/user/address", methods=["GET", "POST"])
def user_address_views():
    form = UserAddressForm()
    if form.validate_on_submit():

        # Check if address id is provided
        address_id = form.data["address_id"]
        if address_id:

            # Try to retrieve address object
            user_address = UserAddress.objects(id=str(address_id))[0]

            # TODO Find a better way to do this
            user_address.address = form.data["address"]
            user_address.address_1 = form.data["address_1"]
            user_address.address_2 = form.data["address_2"]
            user_address.city = form.data["city"]
            user_address.state = form.data["state"]
            user_address.zipcode = form.data["zipcode"]
            user_address.country = form.data["country"]

            # Save address
            user_address.save()

            flash("Address Updated")

            urlencoded_parameters = urllib.parse.urlencode(
                {"address": user_address.id}
            )

            redirect_url = url_for("user_address_views") + \
                "?" + urlencoded_parameters
            return redirect(redirect_url)
        else:
            # Create an address entry for user
            user_address = UserAddress(
                user_id=current_user.id,
                address=form.data["address"],
                address_1=form.data["address_1"],
                address_2=form.data["address_2"],
                city=form.data["city"],
                state=form.data["state"],
                zipcode=form.data["zipcode"],
                country=form.data["country"]
            )

            # Save user model
            user_address.save()

            flash("Address Added")

            return redirect(url_for("index"))
    else:
        # Check if there is a address id in url
        address_id = request.args.get("address", "")

        if address_id:
            user_address = UserAddress.objects(id=address_id)[0]

            # TODO Make sure this work as expected
            if user_address.user_id != current_user.id:
                return abort(404)

            form.address_id.data = str(user_address.id)
            form.address.data = user_address.address
            form.address_1.data = user_address.address_1
            form.address_2.data = user_address.address_2
            form.city.data = user_address.city
            form.state.data = user_address.state
            form.zipcode.data = user_address.zipcode
            form.country.data = user_address.country

            return render_template("users/address.html", form=form, heading="Edit address")

        return render_template("users/address.html", form=form, heading="Add address")
