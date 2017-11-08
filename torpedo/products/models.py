from mongoengine import (
    Document, EmbeddedDocument, StringField, ReferenceField, CASCADE,
    FloatField, IntField, EmbeddedDocumentListField, SequenceField
)

import cloudinary


class Category(Document):
    name = StringField()
    description = StringField()


class ProductAttribute(EmbeddedDocument):
    """
    The ProductAttributes can be embedded directly into the Product model
    """

    id = SequenceField()

    size = StringField()
    color = StringField()

    image = StringField()

    price = FloatField()
    discount = FloatField()
    stock = IntField()

    @property
    def get_image_url(self):
        return cloudinary.utils.cloudinary_url(
            self.image,
            width=50,
            height=50
        )[0]


class Product(Document):
    name = StringField()
    description = StringField()
    category = ReferenceField("products.Category", reverse_delete_rule=CASCADE)

    attributes = EmbeddedDocumentListField(ProductAttribute)
