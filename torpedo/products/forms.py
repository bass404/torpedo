from flask_wtf import Form

from wtforms import TextField, StringField, SelectField

from torpedo.products.models import Category


class ProductForm(Form):
    name = StringField()
    description = TextField()
    category = SelectField(choices=[('test', 'test 1')])

    def __init__(self):
        super().__init__()

        # TODO verify if this works as expected

        # Obtain choices for categories
        categories = Category.objects()

        category_choices = [
            (str(category.id), category.name) for category in categories
        ]

        self.category.choices = category_choices
