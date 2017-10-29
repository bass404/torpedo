from flask import render_template

from torpedo import torpedo_app
from torpedo import mongodb_client


@torpedo_app.route('/login')
def login():
    return render_template("users/login.html")
