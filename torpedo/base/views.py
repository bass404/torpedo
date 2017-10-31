from flask import render_template

from torpedo import torpedo_app


@torpedo_app.route('/')
def index():
    return render_template("base/index.html")


@torpedo_app.route("/contact")
def contact_view():
    return render_template("base/contact.html")
