from flask import render_template, request,url_for, redirect
from flask_login import  current_user,login_required
from torpedo import torpedo_app
from torpedo.products.models import Product
from torpedo.products.helpers import (
    get_category_list, get_products, get_best_sellers
)
from torpedo.products.forms import CommentForm
from torpedo.products.models import Comments

def construct_user_template_dictionary(**kwargs):
    """
    Construct the dictionary that should be user views
    """

    return {
        "sidebar_categories": get_category_list(6),
        "best_selling_products": get_best_sellers(2),
        "similar_products": get_products(3)
    }


@torpedo_app.route("/products/list", methods=["GET", "POST"])
def products_list_view():
    if request.method == "GET":

        # Helper function to return products
        products = get_products(9)

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
    form = CommentForm()
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
        form = form,
        product_image_url=product_image_url,
        **construct_user_template_dictionary()
    )

@torpedo_app.route("/products/detail/comments/<product_id>/", methods=["GET", "POST"])
@torpedo_app.route("/products/detail/comments/<product_id>/<attribute_id>", methods=["GET", "POST"])
@login_required
def add_product_comments(product_id, attribute_id=None):
    form = CommentForm()
    if request.method == "POST":
        # Try to obtain the first item
        comment = Comments(user=current_user.id,comment = form.data["comment"])
        product = Product.objects(id=product_id)[0]
        product.comments.append(comment)

        product.save()

        if attribute_id:
            attribute = product.attributes.filter(id=attribute_id).first()

            if not attribute:
                attribute = product.attributes.filter().first()

        else:
            attribute = product.attributes.filter().first()

    return redirect(url_for('product_detail_view',product_id=product.id,attribute_id=attribute.id))


