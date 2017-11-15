from mongoengine import (
    Document, StringField, EmailField, ReferenceField, CASCADE, DateTimeField
)

from passlib.hash import pbkdf2_sha256


def hash_password(password):
    return pbkdf2_sha256.hash(password)


class User(Document):
    """
    Main user model to use for authentication and login
    """
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    first_name = StringField()
    last_name = StringField()
    phone = StringField()
    date_of_birth = DateTimeField()
    gender_choices = (
        ("M", "Male"),
        ("F", "Female")
    )
    gender = StringField(max_length=1, choices=gender_choices)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_admin(self):
        """
        Check and return true if user has an admin role
        """

        user_role = UserRole.objects(user=self.id)[0]

        if user_role.role_type == UserRole.ROLE_ADMIN:
            return True
        else:
            return False

    def get_id(self):
        return str(self.id)

    def get_name(self):
        if self.first_name and self.last_name:
            return "{} {}".format(self.first_name, self.last_name)
        else:
            return ""

    def set_password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        """
        Verify if password if correct
        """
        return pbkdf2_sha256.verify(password, self.password)

    def get_user_cart(self):
        """
        Return the cart model associated with the user
        """

        # Don't place it at the top of the file in order to avoid cyclic
        # dependency errors
        from torpedo.orders.models import Cart

        cart = Cart.objects.filter(user=self).first()
        return cart

    def get_number_of_items_in_cart(self):
        """
        Return the number of items in the user's cart
        """

        cart = self.get_user_cart()
        if cart:
            return cart.get_number_of_items()
        else:
            return 0


class UserRole(Document):
    """
    Model for user roles
    """
    ROLE_ADMIN = "A"
    ROLE_CUSTOMER = "C"
    role_type_choices = (
        (ROLE_ADMIN, "Admin"),
        (ROLE_CUSTOMER, "Customer")
    )

    role_type = StringField(
        max_length=1,
        choices=role_type_choices,
        required=True,
        default=ROLE_CUSTOMER
    )
    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True, unique=True)

    ROLE_ACTIVE = "A"
    ROLE_INACTIVE = "I"
    status_choices = (
        (ROLE_ACTIVE, "Active"),
        (ROLE_INACTIVE, "Inactive")
    )
    status = StringField(
        max_length=1, choices=status_choices, default=ROLE_ACTIVE)


class AddressMixin():
    """
    Address for user
    """

    address = StringField(required=True)
    address_1 = StringField()
    address_2 = StringField()
    city = StringField(required=True)
    state = StringField()
    zipcode = StringField()
    country = StringField(required=True)


class UserAddress(Document, AddressMixin):

    user = ReferenceField(User, reverse_delete_rule=CASCADE, required=True)
