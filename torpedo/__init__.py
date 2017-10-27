from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient

torpedo_app = Flask(__name__, static_url_path='/static')
torpedo_app.config.from_object('torpedo.config')

login_manager = LoginManager()
login_manager.init_app(torpedo_app)

mongodb_client = MongoClient('localhost', 27017)

# Import views at end to avoid cyclic dependency errors
from torpedo.products import views
from torpedo.users import views
