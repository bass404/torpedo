import os
from flask import Flask, request, render_template
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from torpedo import torpedo_app

app = Flask(__name__)


@torpedo_app.route('/productsUpload', methods=['GET', 'POST'])
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
    return render_template('products/uploadForm.html', upload_result=upload_result, thumbnail_url1=thumbnail_url1,
                           thumbnail_url2=thumbnail_url2)