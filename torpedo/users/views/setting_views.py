from flask import render_template, flash, url_for, redirect, request
from flask_login import login_required, current_user

from torpedo import torpedo_app
from torpedo.users.forms import UserInfoForm


@torpedo_app.route("/user/settings", methods=["GET"])
@login_required
def user_setting_view():
    """
    Return the page for accessing user settings
    """

    return render_template("users/settings/base.html")


@torpedo_app.route("/user/info", methods=["GET", "POST"])
@login_required
def user_info_view():
    """
    View to show and update the current user information
    """

    if request.method == "POST":

        # Initialize form
        form = UserInfoForm()

        if form.validate_on_submit():
            user = current_user

            user.first_name = form.data["first_name"]
            user.last_name = form.data["last_name"]
            user.date_of_birth = form.data["date_of_birth"]
            user.gender = form.data["gender"]
            user.phone = form.data["phone"]

            user.save()

            flash("Information updated")

            return redirect(url_for('user_info_view'))
        else:
            flash("Form validation error")
            return render_template("users/settings/info.html", form=form, heading="Edit Personal Information")

    else:
        # Initialize form
        form = UserInfoForm()

        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.phone.data = current_user.phone
        form.date_of_birth.data = current_user.date_of_birth

        return render_template("users/settings/info.html", form=form, heading="Edit Personal Information")
