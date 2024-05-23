from flask import Blueprint, request, flash, render_template, redirect
from flask_login import login_required

from src.admin.components.users.queries import AdminUsersQueries
from src.admin.utils import check_phone_conf, check_address_conf, check_current_user, check_is_staff, check_email_conf

admin_users_router = Blueprint("admin_users_router", __name__)


@admin_users_router.route("/users")
@login_required
def users_index():
    if check_current_user():
        users = AdminUsersQueries.get_3_last_users()
        staff_users = AdminUsersQueries.get_3_last_staff_users()
        return render_template("admin/users/users.html", title="Пользователи",
                               users=users, staff_users=staff_users)
    return redirect("/")


@admin_users_router.route("/users/all/")
@login_required
def get_all_users():
    if check_current_user():
        users = AdminUsersQueries.get_all_users()
        return render_template("admin/users/all-users.html",
                               users=users, title="Все пользователи")
    return redirect("/")


@admin_users_router.route("/users/staff")
@login_required
def get_all_staff_users():
    if check_current_user():
        users = AdminUsersQueries.get_all_staff_users()
        return render_template("admin/users/all-staff-users.html",
                               users=users, title="Весь персонал")
    return redirect("/")


@admin_users_router.route("/users/<int:user_id>", methods=["GET", "POST"])
@login_required
def get_user_profile(user_id: int):
    if check_current_user():
        if request.method == "POST":
            address_conf = check_address_conf(request.form.get("address_conf_1"), request.form.get("address_conf_2"))
            email_conf = check_email_conf(request.form.get("email_conf"))
            phone_cong = check_phone_conf(request.form.get("phone_conf"))
            is_staff, is_superuser = check_is_staff(request.form.get("is_staff"), request.form.get("is_superuser"))

            detail, status = AdminUsersQueries.update_user(request.files.get("image"), request.form.get("name"),
                                                           request.form.get("surname"), request.form.get("username"),
                                                           request.form.get("address"),
                                                           request.form.get("additional_address"),
                                                           request.form.get("country"), user_id, address_conf,
                                                           email_conf, phone_cong, is_staff, is_superuser)
            if status:
                flash(detail, category="success")
            else:
                flash(detail, category="error")

        user = AdminUsersQueries.get_one_user_by_id(user_id)
        return render_template("admin/users/user-profile.html", user=user,
                               title="Профиль пользователя")
    return redirect("/")