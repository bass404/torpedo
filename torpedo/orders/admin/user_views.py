from flask import render_template, abort, redirect, url_for
from flask_login import current_user, login_required
import time

from torpedo import torpedo_app
from torpedo.products.models import Product
from torpedo.orders.models import ProductAndAttribute, CartProductDetail, Cart, OrderDetail, Order
from torpedo.users.models import UserAddress


@torpedo_app.route("/user/checkout", methods=["GET"])
@login_required
def user_checkout_view():
    # Obtain the products in cart for the user
    cart = Cart.objects(user=current_user.id).first()
    if cart:
        return render_template("orders/checkout.html", products=cart.product_details, cart_details=cart.get_details)
    else:
        return render_template("orders/checkout_empty.html")


@torpedo_app.route("/user/shipping_address", methods=["GET"])
@login_required
def user_order_shipping_view():
    # Obtain the products in cart for the user
    shipping_address = UserAddress.objects(user=current_user.id).first()
    if not shipping_address:
        return render_template("orders/shipping_new.html")
    else:
        return render_template("orders/shipping.html", shipping_address=shipping_address)


@torpedo_app.route("/user/order", methods=["GET"])
@login_required
def user_order_view():
    # Obtain the products in cart for the user
    cart = Cart.objects(user=current_user.id).first()
    return render_template("orders/order.html", products=cart.product_details, cart_details=cart.get_details)


@torpedo_app.route("/user/order/summary", methods=["GET"])
@login_required
def user_ordersummary_view():
    # Obtain the products in cart for the user
    cart = Cart.objects(user=current_user.id).first()
    return render_template("orders/order_summary.html", products=cart.product_details, cart_details=cart.get_details)


@torpedo_app.route("/order/cart/product/add/<product_id>/<attribute_id>/")
@login_required
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
        cart.product_details.append(cart_product_detail)
        cart.save()
    else:
        # Create the Cart object
        cart = Cart(user=current_user.id)
        cart.product_details.append(cart_product_detail)

        # Save the card object
        cart.save()

    return redirect(url_for('user_checkout_view'))


@torpedo_app.route("/order/product/add/")
@login_required
def add_product_to_order():
    # Fetch the cart objects from the session
    cart = Cart.objects(user=current_user.id).first()
    # Create the Order object
    order = Order(user=current_user.id, status='PENDING')
    for each_product_attrb in cart.product_details:
        order_detail = OrderDetail(id=each_product_attrb.id,
            product_and_attribute = each_product_attrb.product_and_attribute,
            price = each_product_attrb.price,
            discount = each_product_attrb.discount,
            quantity = each_product_attrb.quantity)
        order.product_details.append(order_detail)


    # Save the card object
    #TODO: Check for transaction control
    order.save()
    cart.delete()
    #TODO: This can be redirected to a page with a thank you note
    return render_template("orders/order_summary.html", products=order.product_details, order_details=order.get_details)


@torpedo_app.route("/order/cart/product/delete/<product_attribute_id>", methods=["GET"])
@login_required
def product_delete_cart(product_attribute_id):
    # Check if product with the given id exists

    # TODO: handle any exceptions and Check if the cart for user is empty or not

    cart = Cart.objects(user=current_user.id).first()
    cart_product_detail = cart.product_details.filter(id=product_attribute_id)
    cart_product_detail.delete()
    cart.save()

    # Redirect user to checkout page
    return redirect(url_for('user_checkout_view'))
