from mongoengine import (
    Document, StringField, ReferenceField, CASCADE, FloatField, IntField
)


class Category(Document):
    name = StringField()
    description = StringField()


class Product(Document):
    name = StringField()
    description = StringField()
    category = ReferenceField("products.Category", reverse_delete_rule=CASCADE)
    image = StringField()


class ProductAttribute(Document):
    product = ReferenceField("products.Product", reverse_delete_rule=CASCADE)
    size = StringField()
    color = StringField()

    # TODO handle pictures

    price = FloatField()
    discount = FloatField()
    stock = IntField()

