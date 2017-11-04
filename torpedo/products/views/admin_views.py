from flask import render_template, abort, flash, request, redirect, url_for
from flask_login import current_user, login_required

from torpedo import torpedo_app
from torpedo.products.models import Product, Category
from torpedo.products.forms import ProductForm

from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import sys

@torpedo_app.route("/products/admin/add", methods=["GET", "POST"])
@login_required
def add_product_view():
    upload_result = None
    thumbnail_url1 = None
    thumbnail_url2 = None
    if not current_user.is_admin:
        abort(403)
    print("Hello world!!", file=sys.stderr)
    form = ProductForm()
    if request.method == "POST":
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

            # category = Category.objects(id=form.data["category"])[0]

        #     product = Product(
        #         name=form.data["name"],
        #         description=form.data["description"],
        #         category=category.id,
        #         image=upload_result
        #     )
        #     product.save()
        #
        #     flash("Product added")
        #     return redirect(url_for('user_setting_view'))
        # else:
        #     flash("Form validation error")
            return render_template("products/admin/add.html", form=form, heading="Add product", upload_result=upload_result, thumbnail_url1=thumbnail_url1,
                           thumbnail_url2=thumbnail_url2)
    else:
        return render_template("products/admin/add.html", form=form,heading="Add product")


@torpedo_app.route("/productsUpload", methods=["GET", "POST"])
def upload_file():
    upload_result = None
    thumbnail_url1 = None
    thumbnail_url2 = None
    if request.method == 'POST':
        file_to_upload = request.files['file']
        if file_to_upload:
            upload_result = upload(file_to_upload)
            thumbnail_url1, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=100,
                                                     height=100)
            thumbnail_url2, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=200,
                                                     height=100, radius=20, effect="sepia")
    return render_template('products/admin/uploadForm.html', upload_result=upload_result, thumbnail_url1=thumbnail_url1,
                           thumbnail_url2=thumbnail_url2)
