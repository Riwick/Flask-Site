from flask import Blueprint, flash, request, redirect, render_template
from flask_login import login_required
from flask_paginate import get_page_parameter

from src.admin.components.categories.queries import AdminCategoriesQueries
from src.admin.utils import check_current_user
from src.products.utils import get_pagination
from src.utils import get_paginated_staff, PER_PAGE
from src.caching import cache, delete_all_categories_cache

admin_categories_router = Blueprint("admin_categories_router", __name__)


@admin_categories_router.route("/categories")
@login_required
def get_all_categories():
    if check_current_user():
        categories = AdminCategoriesQueries.get_all_categories()

        page = request.args.get(get_page_parameter(), type=int, default=1)
        paginated_categories = get_paginated_staff(
            page=page, staff=categories, per_page=PER_PAGE
        )
        return render_template(
            "admin/categories/categories.html",
            categories=paginated_categories,
            pagination=get_pagination(page=page, per_page=PER_PAGE, total=categories),
            title="Категории",
        )
    return redirect("/")


@admin_categories_router.route(
    "/categories/<int:category_id>/delete", methods=["GET", "POST"]
)
@login_required
def delete_category(category_id: int):
    if check_current_user():
        detail, status = AdminCategoriesQueries.delete_category_by_id(category_id)
        if status:
            flash(detail, category="success")
            delete_all_categories_cache(category_id)
            return redirect(request.referrer)
        else:
            flash(detail, category="error")

    return redirect("/")


@admin_categories_router.route("/categories/add-category", methods=["GET", "POST"])
@login_required
def add_category():
    if check_current_user():
        if request.method == "POST":
            detail, status = AdminCategoriesQueries.add_category(
                request.form["title"], request.form["short_desc"]
            )
            if status:
                flash(detail, category="success")
                cache.delete("categories")
                cache.delete("admin-categories")
            else:
                flash(detail, category="error")

        return render_template(
            "admin/categories/add_category.html", title="Добавление категории"
        )

    return redirect("/")


@admin_categories_router.route(
    "/categories/<int:category_id>", methods=["GET", "POST", "PUT"]
)
@login_required
def update_category(category_id: int):
    if check_current_user():
        if request.method == "POST" or request.method == "PUT":
            detail, status = AdminCategoriesQueries.update_category(
                category_id, request.form["title"], request.form["short_desc"]
            )
            if status:
                flash(detail, category="success")
                delete_all_categories_cache(category_id)
            else:
                flash(detail, category="error")

        category = AdminCategoriesQueries.get_one_category_by_id(category_id)

        return render_template(
            "admin/categories/categories-detail.html",
            category=category,
            title="Обновление категории",
        )

    return redirect("/")
