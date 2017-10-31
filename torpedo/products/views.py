from flask import render_template

from torpedo import torpedo_app


@torpedo_app.route("/products", methods=["GET", "POST"])
def products_list_view():
    return render_template("products/list.html")
