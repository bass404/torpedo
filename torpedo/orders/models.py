from mongoengine import (
    Document, EmbeddedDocument, ReferenceField, FloatField, IntField,
    EmbeddedDocumentListField, EmbeddedDocumentField, SequenceField
)


class ProductAndAttribute(EmbeddedDocument):
    """
    EmbeddedDocument model to store product id and attribute id together
    """

    product = ReferenceField("products.Product")
    product_attribute = IntField()


class BaseOrderDetail(EmbeddedDocument):
    """
    No collection will be created for this model
    """

    id = SequenceField()

    product_and_attribute = EmbeddedDocumentField(
        ProductAndAttribute, required=True)
    price = FloatField(required=True)
    discount = FloatField(default=0.0)
    quantity = IntField(default=1)

    meta = {
        "abstract": True,
    }

    @property
    def get_display_name(self):
        return self.product_and_attribute.product.name

    @property
    def get_image_url(self):
        return self.product_and_attribute.product.get_product_attribute_image_url(
            self.product_and_attribute.product_attribute)

    @property
    def get_size(self):
        return self.product_and_attribute.product.get_product_attribute_size(
            self.product_and_attribute.product_attribute)

    @property
    def get_price(self):
        return self.product_and_attribute.product.get_product_attribute_price(
            self.product_and_attribute.product_attribute)

    @property
    def get_discount(self):
        """
        Return the discount price
        """

        if not self.discount:
            return 0.0

        return self.discount


class CartProductDetail(BaseOrderDetail):
    """
    Store this model in seperate collection
    """
    pass


class Cart(Document):
    """
    Model to hold the cart detail of a user
    """

    user = ReferenceField("users.User")
    product_details = EmbeddedDocumentListField(CartProductDetail)


class OrderDetail(BaseOrderDetail):
    """
    Store this model in seperate collection
    """
    pass


class Order(Document):
    """
    Model to hold the order detail for a user
    """

    user = ReferenceField("users.User")
    product_details = EmbeddedDocumentListField(OrderDetail)
