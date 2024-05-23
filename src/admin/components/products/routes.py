from flask import Blueprint, render_template, redirect, flash, request
from flask_login import login_required
from flask_paginate import get_page_parameter

from src.admin.components.categories.queries import AdminCategoriesQueries
from src.admin.components.products.queries import AdminProductsQueries
from src.admin.utils import check_current_user
from src.products.utils import get_pagination
from src.utils import get_paginated_staff, PER_PAGE

admin_product_router = Blueprint("admin_product_router", __name__)


@admin_product_router.route("/products")
@login_required
def all_products():
    if check_current_user():
        products = AdminProductsQueries.get_all_products()

        page = request.args.get(get_page_parameter(), type=int, default=1)
        paginated_products = get_paginated_staff(page=page, staff=products, per_page=PER_PAGE)
        return render_template("admin/products/products.html", products=paginated_products,
                               title="Продукты", pagination=get_pagination(page=page, per_page=PER_PAGE,
                                                                           total=products))
    return redirect("/")


@admin_product_router.route("/products/<int:product_id>/delete", methods=["GET", "POST", "DELETE"])
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


@admin_product_router.route("/products/add-product", methods=["GET", "POST"])
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


@admin_product_router.route("/products/<int:product_id>", methods=["GET", "POST", "PUT"])
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
