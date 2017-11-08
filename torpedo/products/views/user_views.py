from flask import render_template,request

from torpedo import torpedo_app
from torpedo.products.models import Product


@torpedo_app.route("/products/list", methods=["GET", "POST"])
def products_list_view():
    if request.method == "GET":
        products = Product.objects()
        return render_template("products/list.html",heading="List of products", products=products)


@torpedo_app.route("/products/detail/<product_id>", methods=["GET","POST"])
def product_detail_view(product_id):
    product = Product.objects(id=product_id).first()

    return render_template("products/detail.html",product=product)
