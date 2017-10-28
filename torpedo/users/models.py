from flask_security import UserMixin, RoleMixin

from torpedo import mongodb_client


class Role(mongodb_client.Document, RoleMixin):
    name = mongodb_client.StringField(max_length=80, unique=True)
    description = mongodb_client.StringField(max_length=255)


class User(mongodb_client.Document, UserMixin):
    email = mongodb_client.StringField(max_length=255)
    password = mongodb_client.StringField(max_length=255)
    active = mongodb_client.BooleanField(default=True)
    confirmed_at = mongodb_client.DateTimeField()
    roles = mongodb_client.ListField(
        mongodb_client.ReferenceField(Role), default=[]
    )
