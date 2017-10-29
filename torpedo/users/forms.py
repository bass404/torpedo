from flask_wtf import Form

from wtforms import TextField, StringField, PasswordField


class UserLoginForm(Form):
    """
    Login form for user
    """

    # TODO Missing validation for email
    email = StringField()
    password = PasswordField()
