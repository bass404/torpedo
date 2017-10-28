from flask import Flask

from flask_mongoengine import MongoEngine
from flask_security import UserMixin, RoleMixin
from flask_security import Security, MongoEngineUserDatastore

torpedo_app = Flask(__name__, static_url_path='/static')
torpedo_app.config.from_object('torpedo.config')

# Create database connection
mongodb_client = MongoEngine(torpedo_app)

from torpedo.users.models import User, Role

# Setup Flask-Security
user_datastore = MongoEngineUserDatastore(mongodb_client, User, Role)
security = Security(torpedo_app, user_datastore)

# Import views at end to avoid cyclic dependency errors
from torpedo.products import views
from torpedo.users import views
