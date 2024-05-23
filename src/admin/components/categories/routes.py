from flask import Blueprint, flash, request, redirect, render_template
from flask_login import login_required

from src.admin.components.categories.queries import AdminCategoriesQueries
from src.admin.utils import check_current_user

admin_categories_router = Blueprint("admin_categories_router", __name__)


@admin_categories_router.route("/categories")
@login_required
def get_all_categories():
    if check_current_user():
        categories = AdminCategoriesQueries.get_all_categories()
        return render_template("admin/categories/categories.html", categories=categories,
                               title="Категории")
    return redirect("/")


@admin_categories_router.route("/categories/<int:category_id>/delete", methods=["GET", "POST"])
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


@admin_categories_router.route("/categories/add-category", methods=["GET", "POST"])
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


@admin_categories_router.route("/categories/<int:category_id>", methods=["GET", "POST", "PUT"])
@login_required
def update_category(category_id: int):
    if check_current_user():
        if request.method == "POST" or request.method == "PUT":
            detail, status = AdminCategoriesQueries.update_category(category_id, request.form["title"],
                                                                    request.form["short_desc"])
            if status:
                flash(detail, category="success")
            else:
                flash(detail, category="error")

        category = AdminCategoriesQueries.get_one_category_by_id(category_id)

        return render_template("admin/categories/categories-detail.html", category=category,
                               title="Обновление категории")

    return redirect("/")
