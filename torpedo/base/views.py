from flask import render_template

from torpedo import torpedo_app
from torpedo.products.helpers import get_products


@torpedo_app.route('/')
def index():
    return render_template("base/index.html", new_released_products=get_products(6), featured=get_products(3))


@torpedo_app.route("/contact")
def contact_view():
    return render_template("base/contact.html")
