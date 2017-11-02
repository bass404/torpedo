from flask import render_template, abort
from flask_login import current_user

from torpedo import torpedo_app
from torpedo.products.forms import ProductForm


@torpedo_app.route("/products/admin/add", methods=["GET", "POST"])
def add_product_view():
    if not current_user.is_admin:
        abort(403)

    form = ProductForm()
    return render_template("products/admin/add.html", form=form, heading="Add product")
