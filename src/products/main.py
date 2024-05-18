from flask import Blueprint, render_template, abort, request, redirect, flash
from flask_login import current_user
from flask_paginate import get_page_parameter

from src.products.products_queries import ProductQueries
from src.users.users_queries import UserQueries
from src.products.utils import get_pagination, get_paginated_products

products_router = Blueprint("products_router", __name__, template_folder="templates", static_folder="static")


PER_PAGE = 10


@products_router.route("/", methods=["GET"])
def get_all_products():

    products = ProductQueries.get_all_products_query()
    baskets = UserQueries.get_basket_query(current_user.get_id())

    page = request.args.get(get_page_parameter(), type=int, default=1)
    paginated_products = get_paginated_products(page=page, products=products, per_page=PER_PAGE)

    return render_template("products/products.html",
                           products=paginated_products,
                           title="Каталог", pagination=get_pagination(page=page, per_page=PER_PAGE, total=products),
                           baskets=baskets)


@products_router.route("/<int:product_id>/", methods=["GET"])
def get_one_product(product_id: int):
    product = ProductQueries.get_one_product_query(product_id)
    if not product:
        abort(404)
    return render_template("products/products-detail.html", product=product, title=product.title)


@products_router.route("/add_product/", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        detail, status = ProductQueries.add_product_query(request.form["title"], request.form["short_desc"],
                                                          request.form["desc"],  request.form["price"],
                                                          request.form["cat_id"],  request.files["image"])
        if status:
            flash("Продукт добавлен", category="success")
        else:
            flash(detail, category="error")
    return render_template("products/add_product.html", title="Добавление продукта")


@products_router.route("/<int:product_id>/delete_product/", methods=["DELETE", "POST", "GET"])
def delete_product(product_id: int):
    detail, status = ProductQueries.delete_product_query(product_id)
    if status:
        flash(detail, category="success")
    else:
        flash(detail, category="error")

    return redirect("/products")


