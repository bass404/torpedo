from mongoengine import (
    Document, EmbeddedDocument, StringField, ReferenceField, CASCADE,
    FloatField, IntField, EmbeddedDocumentListField
)


class Category(Document):
    name = StringField()
    description = StringField()


class ProductAttribute(EmbeddedDocument):
    """
    The ProductAttributes can be embedded directly into the Product model
    """

    size = StringField()
    color = StringField()

    image = StringField()

    price = FloatField()
    discount = FloatField()
    stock = IntField()


class Product(Document):
    name = StringField()
    description = StringField()
    category = ReferenceField("products.Category", reverse_delete_rule=CASCADE)

    attributes = EmbeddedDocumentListField(ProductAttribute)
