from flask_wtf import Form

from wtforms import (
    TextField, StringField, SelectField, FileField, FloatField, IntegerField
)
from wtforms.validators import DataRequired

from torpedo.products.models import Category


class CategoryForm(Form):
    name = StringField("name", validators=[DataRequired()])
    description = TextField()

class CommentForm(Form):
    comment = StringField(validators=[DataRequired()])

class ProductForm(Form):
    name = StringField("name", validators=[DataRequired()])
    description = TextField()
    category = SelectField(choices=[])

    def __init__(self):
        super().__init__()

        # Obtain choices for categories
        categories = Category.objects()

        category_choices = [
            (str(category.id), category.name) for category in categories
        ]

        self.category.choices = category_choices


class ProductAttributeForm(Form):
    size = StringField()
    color = StringField()
    image = FileField()
    price = FloatField()
    discount = FloatField()
    stock = IntegerField()
