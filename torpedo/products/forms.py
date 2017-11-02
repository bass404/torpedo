from flask_wtf import Form

from wtforms import TextField, StringField


class ProductForm(Form):
    name = StringField()
    description = TextField()
