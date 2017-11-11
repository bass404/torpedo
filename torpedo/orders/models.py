from datetime import datetime

from mongoengine import (
    Document, EmbeddedDocument, ReferenceField, FloatField, IntField,
    StringField, DateTimeField, EmbeddedDocumentListField,
    EmbeddedDocumentField, SequenceField
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


class OrderDetail(BaseOrderDetail):
    """
    Store this model in seperate collection
    """
    pass


class PriceDetailsMixin():
    """
    Base class for implementing method for price details
    """

    def get_details(self):
        date = datetime.now().strftime("%Y-%m-%d")
        shipping_address = "New Addresss"
        no_items = len(self.product_details)

        total_price = sum([x.get_price for x in self.product_details])
        total_discount = sum([car.get_discount for car in self.product_details])

        shipping_charge = 15
        tax = (total_price + shipping_charge) * 0.15
        net_price = total_price + shipping_charge + tax - total_discount

        shopping_details = {
            "date": date,
            "address": shipping_address,
            "no_items": no_items,
            "total": total_price,
            "discount": total_discount,
            "shipping": shipping_charge,
            "tax": tax,
            "net": net_price
        }

        return shopping_details


class Cart(Document, PriceDetailsMixin):
    """
    Model to hold the cart detail of a user
    """

    user = ReferenceField("users.User")
    product_details = EmbeddedDocumentListField(CartProductDetail)


class Order(Document, PriceDetailsMixin):
    """
    Model to hold the order detail for a user
    """

    user = ReferenceField("users.User")
    product_details = EmbeddedDocumentListField(OrderDetail)
    status = StringField()

    # Don't use function call directly
    # See https://stackoverflow.com/questions/2771676/django-datetime-issues-default-datetime-now
    created_on = DateTimeField(default=datetime.now)
    updated_on = DateTimeField(default=datetime.now)
