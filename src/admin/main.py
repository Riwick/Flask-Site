from flask import Blueprint, redirect
from flask_login import current_user

admin_router = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin_router.route("/")
def index():
    if current_user.is_authenticated and current_user.is_superuser_or_is_staff():
        return "admin"
    return redirect("/")


