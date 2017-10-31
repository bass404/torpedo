from flask_wtf import Form

from wtforms import TextField, StringField, PasswordField, HiddenField


class UserLoginForm(Form):
    """
    Login form for user
    """

    # TODO Missing validation for email
    email = StringField()
    password = PasswordField()


class UserSignupForm(Form):
    """
    Signup form for user
    """

    first_name = StringField()
    last_name = StringField()
    email = StringField()
    password = PasswordField()
    confirm_password = PasswordField()


class UserAddressForm(Form):
    """
    Address form for user
    """
    address_id = HiddenField()

    address = StringField()
    address_1 = StringField()
    address_2 = StringField()
    city = StringField()
    state = StringField()
    zipcode = StringField()
    country = StringField()
