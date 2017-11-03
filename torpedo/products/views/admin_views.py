from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required

from torpedo import torpedo_app
from torpedo.products.models import Product, Category
from torpedo.products.forms import ProductForm, CategoryForm
from torpedo.users.utils import admin_user_required


@torpedo_app.route("/products/admin/add", methods=["GET", "POST"])
@admin_user_required
@login_required
def add_product_view():
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


@torpedo_app.route("/products/admin/list", methods=["GET"])
@admin_user_required
@login_required
def product_list_view():
    # Obtain the list of products
    products = Product.objects()

    return render_template("products/admin/list.html", heading="List of products", products=products)


@torpedo_app.route("/categories/admin/add", methods=["GET", "POST"])
@admin_user_required
@login_required
def add_category_view():
    form = CategoryForm()
    if request.method == "POST":
        if form.validate_on_submit():
            category = Category(
                name=form.data["name"],
                description=form.data["description"]
            )
            category.save()

            flash("Category added")
            return redirect(url_for('user_setting_view'))
        else:
            flash("Could not add category. Form validation error.")
            return render_template("categories/admin/add.html", form=form, heading="Add product")

    else:
        return render_template("categories/admin/add.html", form=form, heading="Add category")


@torpedo_app.route("/categories/admin/list", methods=["GET"])
@admin_user_required
@login_required
def category_list_view():
    # Obtain the list of products
    categories = Category.objects()

    return render_template("categories/admin/list.html", heading="List of categories", categories=categories)
