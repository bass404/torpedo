from torpedo.users.utils import admin_user_required
from torpedo import torpedo_app
from flask_login import login_required
from flask import render_template

from torpedo.orders.models import Order

@torpedo_app.route("/order/admin/list", methods=["GET"])
@login_required
@admin_user_required
def view_order_list():
    # Obtain the list of products
    orders = Order.objects()

    return render_template("orders/admin/list.html", heading="List of orders", orders=orders)
