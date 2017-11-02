from flask import render_template

from torpedo import torpedo_app


@torpedo_app.route("/products/list", methods=["GET", "POST"])
def products_list_view():
    return render_template("products/list.html")


@torpedo_app.route("/products/detail", methods=["GET"])
def product_detail_view():
    return render_template("products/detail.html")
