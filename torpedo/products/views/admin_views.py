from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required

from torpedo import torpedo_app
from torpedo.products.models import Product, Category
from torpedo.products.forms import ProductForm, CategoryForm
from torpedo.users.utils import admin_user_required

from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url


@torpedo_app.route("/products/admin/add", methods=["GET", "POST"])
@admin_user_required
@login_required
def add_product_view():
    upload_result = None
    thumbnail_url1 = None
    thumbnail_url2 = None
    form = ProductForm()
    if request.method == "POST":

        # TODO Fix this
        # if form.validate_on_submit():
        file_to_upload = request.files['file']
        if file_to_upload:
            upload_result = upload(file_to_upload)
            thumbnail_url1, options = cloudinary_url(upload_result['public_id'], format="jpg",
                                                     crop="fill", width=100,
                                                     height=100)
            thumbnail_url2, options = cloudinary_url(upload_result['public_id'], format="jpg",
                                                     crop="fill", width=200,
                                                     height=100, radius=20, effect="sepia")

            category = Category.objects(id=form.data["category"])[0]

            product = Product(
                name=form.data["name"],
                description=form.data["description"],
                category=category.id,
                image=upload_result.get("secure_url", "")
            )
            product.save()

            flash("Product added")
            return redirect(url_for('user_setting_view'))
        else:
            flash("Form validation error")
            return render_template("products/admin/add.html", form=form, heading="Add product", upload_result=upload_result, thumbnail_url1=thumbnail_url1,
                                   thumbnail_url2=thumbnail_url2)
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
