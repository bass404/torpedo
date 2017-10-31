from flask import render_template

from torpedo import torpedo_app


@torpedo_app.route('/')
def index():
    return render_template("index.html")
