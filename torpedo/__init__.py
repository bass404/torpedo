from flask import Flask

torpedo_app = Flask(__name__)

from torpedo.products import views
