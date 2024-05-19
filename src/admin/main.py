from flask import Blueprint, redirect, render_template
from flask_login import current_user, login_required

from src.admin.admin_queries import AdminQueries, AdminUsersQueries
from src.admin.utils import check_current_user

admin_router = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin_router.route("/")
@login_required
def index():
    if check_current_user():
        products = AdminQueries.get_3_last_products_for_main_page()
        feedbacks = AdminQueries.get_3_last_feedbacks_for_main_page()
        return render_template("admin/index.html",
                               products=products, feedbacks=feedbacks)
    return redirect("/")


"""Роуты продуктов"""


@admin_router.route("/products")
@login_required
def all_products():
    if check_current_user():
        products = AdminQueries.get_all_products()
        return render_template("admin/products/products.html",
                               products=products, title="Продукты")
    return redirect("/")


@admin_router.route("/products/<int:product_id>", methods=["GET", "POST"])
@login_required
def get_one_product(product_id: int):
    if check_current_user():
        products = AdminQueries.get_all_products()
        return render_template("admin/products/products-detail.html",
                               products=products, title=f"Продукт - {product_id}")
    return redirect("/")


"""Роуты обратной связи"""


@admin_router.route("/feedbacks")
@login_required
def all_feedbacks():
    if check_current_user():
        feedbacks = AdminQueries.get_all_feedbacks()
        return render_template("admin/feedbacks/feedbacks.html",
                               feedbacks=feedbacks, title="Обращения")
    return redirect("/")


"""Роуты пользователей"""


@admin_router.route("/users")
@login_required
def users_index():
    if check_current_user():
        users = AdminUsersQueries.get_3_last_users()
        staff_users = AdminUsersQueries.get_3_last_staff_users()
        return render_template("admin/users/users.html", title="Пользователи",
                               users=users, staff_users=staff_users)
    return redirect("/")


@admin_router.route("/users/all/")
@login_required
def get_all_users():
    if check_current_user():
        users = AdminUsersQueries.get_all_users()
        return render_template("admin/users/all-users.html",
                               users=users, title="Все пользователи")
    return redirect("/")


@admin_router.route("/users/staff")
@login_required
def get_all_staff_users():
    if check_current_user():
        users = AdminUsersQueries.get_all_staff_users()
        return render_template("admin/users/all-staff-users.html",
                               users=users, title="Весь персонал")
    return redirect("/")
