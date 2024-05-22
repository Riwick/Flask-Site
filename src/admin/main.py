from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import current_user, login_required

from src.admin.admin_queries import AdminProductsQueries, AdminUsersQueries, AdminCategoriesQueries, \
    AdminFeedbacksQueries
from src.admin.utils import check_current_user
from src.products.products_queries import ProductQueries

admin_router = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin_router.route("/")
@login_required
def index():
    if check_current_user():
        products = AdminProductsQueries.get_3_last_products_for_main_page()
        feedbacks = AdminFeedbacksQueries.get_3_last_feedbacks_for_main_page()
        categories = AdminCategoriesQueries.get_3_last_categories_for_main_page()
        return render_template("admin/index.html",
                               products=products, feedbacks=feedbacks, categories=categories)
    return redirect("/")


"""Роуты продуктов"""


@admin_router.route("/products")
@login_required
def all_products():
    if check_current_user():
        products = AdminProductsQueries.get_all_products()
        return render_template("admin/products/products.html",
                               products=products, title="Продукты")
    return redirect("/")


@admin_router.route("/products/<int:product_id>/delete", methods=["GET", "POST", "DELETE"])
@login_required
def delete_product(product_id: int):
    if check_current_user():
        detail, status = AdminProductsQueries.delete_product(product_id)
        if status:
            flash(detail, category="success")
            return redirect(request.referrer)
        else:
            flash(detail, category="error")
    return redirect("/")


@admin_router.route("/products/add-product", methods=["GET", "POST"])
@login_required
def add_product():
    if check_current_user():
        if request.method == "POST":
            detail, status = AdminProductsQueries.add_product(request.form["title"], request.form["short_desc"],
                                                              request.form["desc"], request.form["price"],
                                                              request.form["cat_name"], request.files["image"])
            if status:
                flash(detail, category="success")
            else:
                flash(detail, category="error")

        categories = AdminCategoriesQueries.get_all_categories()
        return render_template("admin/products/add_product.html", categories=categories)

    return redirect("/")


@admin_router.route("/products/<int:product_id>", methods=["GET", "POST", "PUT"])
@login_required
def update_product(product_id: int):
    if check_current_user():
        if request.method == "POST" or request.method == "PUT":
            detail, status = AdminProductsQueries.update_product(product_id, request.form["title"],
                                                                 request.form["short_desc"],
                                                                 request.form["desc"], request.form["price"],
                                                                 request.form["cat_name"], request.files["image"])
            if status:
                flash(detail, category="success")
            else:
                flash(detail, category="error")

        categories = AdminCategoriesQueries.get_all_categories()
        product = AdminProductsQueries.get_one_product_by_id(product_id)

        return render_template("admin/products/products-detail.html", categories=categories,
                               product=product, title=f"Обновление продукта - {product.title}")

    return redirect("/")


"""Роуты обратной связи"""


@admin_router.route("/feedbacks")
@login_required
def all_feedbacks():
    if check_current_user():
        feedbacks = AdminFeedbacksQueries.get_all_feedbacks()
        return render_template("admin/feedbacks/feedbacks.html",
                               feedbacks=feedbacks, title="Обращения")
    return redirect("/")


@admin_router.route("/feedbacks/<int:feedback_id>/delete", methods=["GET", "POST", "DELETE"])
@login_required
def delete_feedback(feedback_id: int):
    if check_current_user():
        detail, status = AdminFeedbacksQueries.delete_feedback(feedback_id)
        if status:
            flash(detail, category="success")
            return redirect(request.referrer)
        else:
            flash(detail, category="error")

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


"""Роуты категорий"""


@admin_router.route("/categories")
@login_required
def get_all_categories():
    if check_current_user():
        categories = AdminCategoriesQueries.get_all_categories()
        return render_template("admin/categories/categories.html", categories=categories,
                               title="Категории")
    return redirect("/")


@admin_router.route("/categories/<int:category_id>/delete", methods=["GET", "POST"])
@login_required
def delete_category(category_id: int):
    if check_current_user():
        detail, status = AdminCategoriesQueries.delete_category_by_id(category_id)
        if status:
            flash(detail, category="success")
            return redirect(request.referrer)
        else:
            flash(detail, category="error")

    return redirect("/")


@admin_router.route("/categories/add-category", methods=["GET", "POST"])
@login_required
def add_category():
    if check_current_user():
        if request.method == "POST":
            detail, status = AdminCategoriesQueries.add_category(request.form["title"], request.form["short_desc"])
            if status:
                flash(detail, category="success")
            else:
                flash(detail, category="error")

        return render_template("admin/categories/add_category.html", title="Добавление категории")

    return redirect("/")
