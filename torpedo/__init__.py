from flask import Flask
from flask_login import LoginManager

from mongoengine import connect

torpedo_app = Flask(__name__, static_url_path='/static')
torpedo_app.config.from_object('torpedo.config')

login_manager = LoginManager()
login_manager.init_app(torpedo_app)
login_manager.login_view = "login"

# Connect to MongoDB
connect(
    db="torpedo"
)

# Import views at end to avoid cyclic dependency errors
from torpedo.base import views as base_views
from torpedo.users import views as user_views
from torpedo.products import views as product_views
from torpedo.orders import views as order_views
