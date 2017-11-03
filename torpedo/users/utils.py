from functools import wraps

from flask import abort

from flask_login import current_user


def admin_user_required(view_function):
    """
    Decorated to determine if current_user has admin role and deny access to
    view is is not an admin user
    """

    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)

        return view_function(*args, **kwargs)

    return wrapper
