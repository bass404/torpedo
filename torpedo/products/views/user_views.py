import random

from flask import render_template, request

from torpedo import torpedo_app
from torpedo.products.models import Product
from torpedo.products.helpers import get_category_list


def construct_user_template_dictionary(**kwargs):
    """
    Construct the dictionary that should be user views
    """

    return {
        "sidebar_categories": get_category_list(6)
    }


@torpedo_app.route("/products/list", methods=["GET", "POST"])
def products_list_view():
    if request.method == "GET":
        products = Product.objects()

        # NOTE when enough products are inserted remove this later
        number_of_products = len(products)
        if number_of_products < 9:
            products = [product for product in products]
            for i in range(0, 9 - number_of_products):
                # Randomly insert items into list to make it longer
                products.append(
                    products[random.randint(0, number_of_products - 1)])

        return render_template(
            "products/list.html",
            heading="List of products",
            products=products,
            **construct_user_template_dictionary()
        )


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

    return render_template(
        "products/detail.html",
        heading="List of products",
        product=product,
        attribute=attribute,
        product_image_url=product_image_url,
        **construct_user_template_dictionary()
    )
