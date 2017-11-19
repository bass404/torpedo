from mongoengine import (
    Document, EmbeddedDocument, StringField, ReferenceField, CASCADE,
    FloatField, IntField, EmbeddedDocumentListField, SequenceField,DateTimeField
)
from datetime import datetime
import cloudinary


class Category(Document):
    name = StringField()
    description = StringField()

class Comments(EmbeddedDocument):
    user = ReferenceField("users.User")
    comment = StringField()
    created_on = DateTimeField(default=datetime.now)
    updated_on = DateTimeField(default=datetime.now)

    #https: // stackoverflow.com / questions / 43553222 / transform - datetime - in -yyyy - mm - dd - hhmmss - ssssss
    #Format check : https://jeffkayser.com/projects/date-format-string-composer/index.html
    @property
    def get_comment_date(self):
        dtObject = datetime.strptime(str(self.created_on),"%Y-%m-%d %H:%M:%S.%f")
        return dtObject.strftime("%B %e, %Y")

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
        return cloudinary.utils.cloudinary_url(self.image)[0]

    @property
    def generate_display_name(self):
        return "{} - {}".format(self.color, self.size)


class Product(Document):
    name = StringField()
    description = StringField()
    category = ReferenceField("products.Category", reverse_delete_rule=CASCADE)
    comments = EmbeddedDocumentListField(Comments)
    attributes = EmbeddedDocumentListField(ProductAttribute)

    @property
    def get_Description(self):
        """
        Return the short product description of first url
        """

        if not self.description:
            return ""

        description = self.description
        info = (description[:30] + '...') if len(description) > 30 else description
        return info

    @property
    def get_price(self):
        """
        Return the short product description of first url
        """

        if not self.attributes[0].price:
            return ""

        return self.attributes[0].price

    @property
    def get_image_url(self):
        """
        Return the image url of first url
        """

        if not self.attributes:
            return ""

        attribute = self.attributes[0]
        return attribute.get_image_url

    def get_product_attribute_image_url(self, attribute_id):

        # Obtain attribute
        attribute = self.attributes.filter(id=attribute_id).first()
        return attribute.get_image_url

    def get_product_attribute_size(self, attribute_id):

        # Obtain attribute
        attribute = self.attributes.filter(id=attribute_id).first()
        return attribute.size

    def get_product_attribute_price(self, attribute_id):

        # Obtain attribute
        attribute = self.attributes.filter(id=attribute_id).first()
        return attribute.price

    def get_product_attribute_property(self, attribute_id, attribute_key):
        """
        Generalized function to obtain the property from attribute
        """

        # Obtain attribute
        attribute = self.attributes.filter(id=attribute_id).first()

        try:
            attribute_value = attribute.__getitem__(attribute_key)
        except KeyError:
            return None

        return attribute_value
