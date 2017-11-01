import urllib

from flask import render_template, request, flash, redirect, url_for, abort
from flask_login import current_user, login_required

from torpedo import torpedo_app

from torpedo.users.models import UserAddress
from torpedo.users.forms import UserAddressForm


@torpedo_app.route("/user/address/list", methods=["GET"])
@login_required
def user_address_list_view():
    """
    Return the user address list
    """

    # Obtain the address items for current_user
    user_addresses = UserAddress.objects(user_id=current_user.id)

    return render_template(
        "users/address/list.html",
        addresses=user_addresses,
        heading="List of addresses"
    )


@torpedo_app.route("/user/address/", methods=["GET", "POST"])
@login_required
def user_address_views():
    form = UserAddressForm()
    if request.method == "POST":
        if form.validate_on_submit():

            # Check if address id is provided
            address_id = form.data["address_id"]
            if address_id:

                # Try to retrieve address object
                user_address = UserAddress.objects(id=str(address_id))[0]

                # TODO Find a better way to do this
                user_address.address = form.data["address"]
                user_address.address_1 = form.data["address_1"]
                user_address.address_2 = form.data["address_2"]
                user_address.city = form.data["city"]
                user_address.state = form.data["state"]
                user_address.zipcode = form.data["zipcode"]
                user_address.country = form.data["country"]

                # Save address
                user_address.save()

                flash("Address Updated")

                urlencoded_parameters = urllib.parse.urlencode(
                    {"address": user_address.id}
                )

                redirect_url = url_for("user_address_views") + \
                    "?" + urlencoded_parameters
                return redirect(redirect_url)
            else:
                # Create an address entry for user
                user_address = UserAddress(
                    user_id=current_user.id,
                    address=form.data["address"],
                    address_1=form.data["address_1"],
                    address_2=form.data["address_2"],
                    city=form.data["city"],
                    state=form.data["state"],
                    zipcode=form.data["zipcode"],
                    country=form.data["country"]
                )

                # Save user model
                user_address.save()

                flash("Address Added")

                return redirect(url_for("index"))
        else:
            flash("Form validation error")
            return render_template("users/address/detail.html", form=form, heading="Edit address")
    else:
        # Check if there is a address id in url
        address_id = request.args.get("address", "")

        if address_id:
            user_address = UserAddress.objects(id=address_id)[0]

            if user_address.user_id.id != current_user.id:
                return abort(404)

            form.address_id.data = str(user_address.id)
            form.address.data = user_address.address
            form.address_1.data = user_address.address_1
            form.address_2.data = user_address.address_2
            form.city.data = user_address.city
            form.state.data = user_address.state
            form.zipcode.data = user_address.zipcode
            form.country.data = user_address.country

        return render_template("users/address/detail.html", form=form, heading="Edit address")
