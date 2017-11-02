from flask import render_template, abort, flash, request, redirect, url_for
from flask_login import current_user, login_required

from torpedo import torpedo_app
from torpedo.products.models import Product, Category
from torpedo.products.forms import ProductForm


@torpedo_app.route("/products/admin/add", methods=["GET", "POST"])
@login_required
def add_product_view():
    if not current_user.is_admin:
        abort(403)

    form = ProductForm()
    if request.method == "POST":
        if form.validate_on_submit():
            category = Category.objects(id=form.data["category"])[0]

            product = Product(
                name=form.data["name"],
                description=form.data["description"],
                category=category.id
            )
            product.save()

            flash("Product added")
            return redirect(url_for('user_setting_view'))
        else:
            flash("Form validation error")
            return render_template("products/admin/add.html", form=form, heading="Add product")
    else:
        return render_template("products/admin/add.html", form=form, heading="Add product")
