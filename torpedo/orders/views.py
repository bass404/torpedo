from flask import render_template
from flask_login import current_user, login_required

from torpedo import torpedo_app


@torpedo_app.route("/user/checkout", methods=["GET"])
@login_required
def user_checkout_view():
    return render_template("orders/checkout.html")
