from torpedo import torpedo_app

from flask import render_template
from flask_login import login_required


@torpedo_app.route("/user/settings", methods=["GET"])
@login_required
def user_setting_view():
    """
    Return the page for accessing user settings
    """

    return render_template("users/settings/base.html")
