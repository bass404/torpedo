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


class ProductAttribute(Document):
    product = ReferenceField("products.Product", reverse_delete_rule=CASCADE)
    size = StringField()
    color = StringField()

    image = StringField()

    price = FloatField()
    discount = FloatField()
    stock = IntField()
