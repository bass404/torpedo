from flask_wtf import Form

from wtforms import (
    TextField, StringField, PasswordField, HiddenField, DateField, SelectField
)

from torpedo.users.models import User


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


class UserInfoForm(Form):
    """
    Form to update the user information
    """

    first_name = StringField()
    last_name = StringField()
    date_of_birth = DateField()
    gender = SelectField(choices=User.gender_choices)
    phone = StringField()


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
