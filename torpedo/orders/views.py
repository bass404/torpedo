from flask import render_template, abort, redirect, url_for
from flask_login import current_user, login_required

from torpedo import torpedo_app
from torpedo.products.models import Product
from torpedo.orders.models import ProductAndAttribute, CartProductDetail, Cart


@torpedo_app.route("/user/checkout", methods=["GET"])
@login_required
def user_checkout_view():
    return render_template("orders/checkout.html")


@torpedo_app.route("/order/cart/product/add/<product_id>/<attribute_id>/")
def add_product_to_cart(product_id, attribute_id):
    # Fetch the product
    product = Product.objects(id=product_id)[0]

    if not product:
        abort(404)

    product_attribute = product.attributes.filter(id=attribute_id)[0]

    if not product_attribute:
        abort(404)

    # Construct the ProductAndAttribute object
    product_and_attribute = ProductAndAttribute(
        product=product.id,
        product_attribute=product_attribute.id
    )

    # Create the CartProductDetail object
    cart_product_detail = CartProductDetail(
        product_and_attribute=product_and_attribute,
        price=product_attribute.price,
        discount=product_attribute.discount
    )

    # Check if a cart for user already exits
    cart = Cart.objects(user=current_user.id).first()
    if cart:
        cart.cart_product_details.append(cart_product_detail)
        cart.save()
    else:
        # Create the Cart object
        cart = Cart(user=current_user.id)
        cart.cart_product_details.append(cart_product_detail)

        # Save the card object
        cart.save()

    return redirect(url_for('products_list_view'))
