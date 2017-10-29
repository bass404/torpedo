from flask_wtf import Form

from wtforms import TextField, StringField, PasswordField


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
