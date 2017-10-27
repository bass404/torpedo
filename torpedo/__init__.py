from flask import Flask

torpedo_app = Flask(__name__, static_url_path='/static')

from torpedo.products import views
