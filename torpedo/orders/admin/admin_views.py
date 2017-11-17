from torpedo.users.utils import admin_user_required
from torpedo import torpedo_app
from flask_login import login_required,current_user
from flask import render_template

from torpedo.orders.models import Order
from datetime import datetime

@torpedo_app.route("/order/admin/list", methods=["GET"])
@login_required
@admin_user_required
def view_order_list():
    # Obtain the list of products
    orders = Order.objects()

    return render_template("orders/admin/collapse.html", heading="List of orders", orders=orders)


#TODO: This url just requires POST request. Try removing GET request
@torpedo_app.route("/order/status/change/<order_id>/<status>", methods=["GET","POST"])
@login_required
@admin_user_required
def order_status_change(order_id,status):
    # Obtain the list of products
    order = Order.objects(id=order_id).first()
    order.status = status
    order.updated_on = datetime.now
    order.save()
    orders = Order.objects()

    return render_template("orders/admin/collapse.html", heading="List of orders", orders=orders)



@torpedo_app.route("/order/list/<order_id>", methods=["GET"])
def order_detail(order_id):
    #TODO: have to do pagination from query
    order = Order.objects(id=order_id).first()
    price_details = order.get_details()
    return render_template("orders/admin/detail.html", heading="Order detail",order = order, price_details=price_details)


