from mongoengine import Document, StringField, EmailField


class User(Document):
    first_name = StringField()
    last_name = StringField()
    email = EmailField()
    password = StringField()

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
        return self.id
