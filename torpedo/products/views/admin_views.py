from flask import render_template, flash, request, redirect, url_for, abort
from flask_login import login_required

from torpedo import torpedo_app
from torpedo.products.models import Product, Category, ProductAttribute
from torpedo.products.forms import ProductForm, CategoryForm, ProductAttributeForm
from torpedo.users.utils import admin_user_required

from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url


@torpedo_app.route("/products/admin/add", methods=["GET", "POST"])
@login_required
@admin_user_required
def add_product_view():
    form = ProductForm()
    if request.method == "POST":

        if form.validate_on_submit():

            # TODO Find if there is an alternative
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
@login_required
@admin_user_required
def product_list_view():
    # Obtain the list of products
    products = Product.objects()

    return render_template("products/admin/list.html", heading="List of products", products=products)


@torpedo_app.route("/products/attributes/admin/add/<product_id>", methods=["GET", "POST"])
@login_required
@admin_user_required
def product_attributes_add_view(product_id):
    # Check if product with the given id exists
    product = Product.objects(id=product_id)[0]

    form = ProductAttributeForm()

    if not product:
        abort(404)

    if request.method == "POST":

        if form.validate_on_submit():

            # Upload the image to cloudinary
            file_to_upload = request.files['image']

            upload_result = upload(file_to_upload)

            product_attribute = ProductAttribute(
                size=form.data["size"],
                color=form.data["color"],
                image=upload_result.get("secure_url", ""),
                price=form.data["price"],
                discount=form.data["discount"],
                stock=form.data["stock"]
            )

            product.attributes.append(product_attribute)
            product.save()

            flash("Product attribute added")
            return redirect(url_for("product_update_view", product_id=product.id))

        else:
            flash("Form validation error")
            return render_template("products/attributes/admin/add.html", product=product, form=form)

    else:
        return render_template("products/attributes/admin/add.html", product=product, form=form)


@torpedo_app.route("/products/attributes/admin/update/<product_id>/<attribute_id>", methods=["GET"])
@login_required
@admin_user_required
def product_attribute_update_view(product_id, attribute_id):
    if request.method == "GET":

        # Check if product with the given id exists
        product = Product.objects(id=product_id)[0]

        if not product:
            abort(404)

        # Obtain corresponding attribute
        attribute = product.attributes.filter(id=attribute_id)

        attribute.delete()

        # Save changes to database
        product.save()

        return redirect(url_for('product_update_view', product_id=product.id))


@torpedo_app.route("/products/admin/update/<product_id>", methods=["GET", "POST"])
@login_required
@admin_user_required
def product_update_view(product_id):

    # Check if product with the given id exists
    product = Product.objects(id=product_id)[0]
    if not product:
        abort(404)

    form = ProductForm()

    if request.method == "POST":

        if form.validate_on_submit():

            # TODO Find if there is an alternative
            category = Category.objects(id=form.data["category"])[0]

            product.name = form.data["name"]
            product.description = form.data["description"]

            product.category = category

            product.save()

            flash("Product Detail updated")

            return redirect(url_for("product_update_view", product_id=product.id))

        else:
            flash("Form validation error")
            return redirect(url_for("product_update_view", product_id=product.id))

    else:
        form.name.data = product.name
        form.description.data = product.description
        form.category.data = product.category

        return render_template(
            "products/admin/update.html",
            heading="Product detail",
            product=product,
            form=form
        )


@torpedo_app.route("/categories/admin/add", methods=["GET", "POST"])
@login_required
@admin_user_required
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
@login_required
@admin_user_required
def category_list_view():
    # Obtain the list of products
    categories = Category.objects()

    return render_template("categories/admin/list.html", heading="List of categories", categories=categories)
