from flask import render_template, abort, redirect, url_for, request
from flask_login import current_user, login_required
import time

from torpedo import torpedo_app
from torpedo.products.models import Product
from torpedo.orders.models import ProductAndAttribute, ProductDetail, Cart, Order, OrderAddress
from torpedo.users.models import UserAddress
from torpedo.users.forms import UserAddressForm


@torpedo_app.route("/user/checkout", methods=["GET"])
@login_required
def user_checkout_view():
    # Obtain the products in cart for the user
    cart = Cart.objects(user=current_user.id).first()
    if cart:
        cart.shipping_address = ""
        if cart.product_details:
            return render_template("orders/checkout.html", products=cart.product_details, cart_details=cart.get_details())

    return render_template("orders/checkout_empty.html")


@torpedo_app.route("/user/shipping_address/<add_new>", methods=["GET", "POST"])
@login_required
def user_order_shipping_view(add_new):
    # Obtain the products in cart for the user
    #shipping_address = UserAddress.objects(user=current_user.id).first()
    user_addresses = UserAddress.objects(user=current_user.id)
    if user_addresses and add_new == 'p':
        return render_template("orders/shipping.html", addresses=user_addresses, user=current_user)
    else:

        form = UserAddressForm()

        if request.method == "POST":
            # Create an address entry for user
            user_address = UserAddress(
                user=current_user.id,
                address=form.data["address"],
                address_1=form.data["address_1"],
                address_2=form.data["address_2"],
                city=form.data["city"],
                state=form.data["state"],
                zipcode=form.data["zipcode"],
                country=form.data["country"]
            )

            # Save user model
            user_address.save()

            return redirect(url_for("user_order_shipping_view",add_new="p"))
        else:
            return render_template("orders/shipping_new.html", form=form, heading="Add shipping address")


@torpedo_app.route("/user/shipping_address_modify/<address_id>", methods=["GET", "POST"])
@login_required
def modify_shipping_address_view(address_id):
    shipping_address = UserAddress.objects(id=address_id)[0]
    if shipping_address:

        form = UserAddressForm()

        if request.method == "POST":
            # Create an address entry for user
            if form.validate_on_submit():
                user_address = UserAddress.objects(id=str(address_id))[0]

                # TODO Find a better way to do this
                user_address.address = form.data["address"]
                user_address.address_1 = form.data["address_1"]
                user_address.address_2 = form.data["address_2"]
                user_address.city = form.data["city"]
                user_address.state = form.data["state"]
                user_address.zipcode = form.data["zipcode"]
                user_address.country = form.data["country"]

                # Save address
                user_address.save()

                return redirect(url_for("user_order_shipping_view",add_new="p"))
        else:

            user_address = UserAddress.objects(id=address_id)[0]

            if user_address.user.id != current_user.id:
                return abort(404)

            form.address_id.data = str(user_address.id)
            form.address.data = user_address.address
            form.address_1.data = user_address.address_1
            form.address_2.data = user_address.address_2
            form.city.data = user_address.city
            form.state.data = user_address.state
            form.zipcode.data = user_address.zipcode
            form.country.data = user_address.country

            return render_template("orders/shipping_new.html", form=form, heading="Add shipping address")


@torpedo_app.route("/user/order", methods=["GET", "POST"])
@login_required
def user_order_view():
    # Obtain the products in cart for the user
    if request.method == "POST":
        address_id = request.form['optradio']
        btnValue = request.form['submitBtn']
        if btnValue == "Place Order":
            cart = Cart.objects(user=current_user.id).first()
            shipping_address = UserAddress.objects(id=address_id)[0]
            if shipping_address:
                return render_template("orders/order.html", products=cart.product_details, cart_details=cart.get_details(), user=current_user, shipping_address=shipping_address)

        elif btnValue == "Edit Shipping Address":
            return redirect(url_for('modify_shipping_address_view',address_id=address_id))


@torpedo_app.route("/user/order/summary/<address_id>", methods=["GET", "POST"])
@login_required
def user_ordersummary_view(address_id):
    # Obtain the products in cart for the user
    cart = Cart.objects(user=current_user.id).first()
    shipping_address = UserAddress.objects(id=address_id)[0]
    if shipping_address:
        return render_template("orders/order_summary.html", products=cart.product_details, cart_details=cart.get_details(), user=current_user, shipping_address=shipping_address)


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

    # Create the ProductDetail object
    cart_product_detail = ProductDetail(
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


@torpedo_app.route("/order/product/add/<address_id>")
@login_required
def add_product_to_order(address_id):
    # Fetch the cart objects from the session
    cart = Cart.objects(user=current_user.id).first()

    # Obtain the address object for the user
    address_obj = UserAddress.objects(user=current_user.id, id=address_id).first()

    # Copy the attributes to OrderAddress
    # NOTE operator overloading might be useful
    orderaddress_obj = OrderAddress(
        address=address_obj.address,
        address_1=address_obj.address_1,
        address_2=address_obj.address_2,
        city=address_obj.city,
        state=address_obj.state,
        zipcode=address_obj.zipcode,
        country=address_obj.country
    )

    # Create the Order object
    order = Order(user=current_user.id, status='PENDING', address=orderaddress_obj)
    for each_product_attrb in cart.product_details:

        #TODO: FIND efficient way than this
        product = Product.objects(id = each_product_attrb.product_and_attribute.product.id).first()
        for attribute in product.attributes:
            if attribute.id == each_product_attrb.product_and_attribute.product_attribute:
                if attribute.stock <=0:
                    return #TODO: Add a viewing message
                attribute.stock = attribute.stock - 1
        product.save()

        order_detail = ProductDetail(id=each_product_attrb.id,
                                   product_and_attribute=each_product_attrb.product_and_attribute,
                                   price=each_product_attrb.price,
                                   discount=each_product_attrb.discount,
                                   quantity=each_product_attrb.quantity)

        order.product_details.append(order_detail)

    # Save the card object
    # TODO: Check for transaction control
    order.save()
    cart.delete()

    # TODO: This can be redirected to a page with a thank you note
    shipping_address = UserAddress.objects(id=address_id)[0]
    return render_template("orders/order_summary.html", products=order.product_details,
                           order_details=order.get_details(), user=current_user, shipping_address=shipping_address, order_id=order.id)


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

@torpedo_app.route("/order/user/list/", methods=["GET"])
def user_order_detail():
    #TODO: have to do pagination from query
    orders = Order.objects(user=current_user.id)
    return render_template("orders/admin/user_detail.html", heading="Order detail",orders = orders)

