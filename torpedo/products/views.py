from flask import render_template

from torpedo import torpedo_app


@torpedo_app.route('/')
def index():
    return render_template("index.html")


@torpedo_app.route('/login')
def login():
    return render_template("login.html")
