from flask import render_template, request

from torpedo import torpedo_app
from torpedo.products.models import Product


@torpedo_app.route("/products/list", methods=["GET", "POST"])
def products_list_view():
    if request.method == "GET":
        products = Product.objects()
        return render_template("products/list.html", heading="List of products", products=products)


@torpedo_app.route("/products/detail/<product_id>/", methods=["GET", "POST"])
@torpedo_app.route("/products/detail/<product_id>/<attribute_id>", methods=["GET", "POST"])
def product_detail_view(product_id, attribute_id=None):
    # Try to obtain the first item
    product = Product.objects(id=product_id)[0]

    if attribute_id:
        attribute = product.attributes.filter(id=attribute_id).first()

        if not attribute:
            attribute = product.attributes.filter().first()

    else:
        attribute = product.attributes.filter().first()

    product_image_url = product.get_product_attribute_image_url(attribute.id)

    return render_template("products/detail.html", product=product, attribute=attribute, product_image_url=product_image_url)
