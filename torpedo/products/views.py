from flask import render_template

from torpedo import torpedo_app

from .productAdd_view import *

@torpedo_app.route('/')
def index():
    return render_template("index.html")
