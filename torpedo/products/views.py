from flask import render_template
from flask_security import login_required

from torpedo import torpedo_app, mongodb_client


@torpedo_app.route('/')
def index():
    return render_template("index.html")
