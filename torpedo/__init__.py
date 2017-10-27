from flask import Flask

torpedo_app = Flask(__name__, static_url_path='/static')
torpedo_app.config.from_object('config')

# Import views at end to avoid cyclic dependency errors
from torpedo.products import views
