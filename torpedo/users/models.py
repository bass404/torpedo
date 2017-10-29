from mongoengine import Document, StringField, EmailField

from passlib.hash import pbkdf2_sha256


def hash_password(password):
    return pbkdf2_sha256.hash(password)


class User(Document):
    first_name = StringField()
    last_name = StringField()
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def set_password(self, password):
        self.password = hash_password(password)

    def check_password(self, password):
        """
        Verify if password if correct
        """

        password_hash = hash_password(password)
        return pbkdf2_sha256.verify(password, password_hash)
