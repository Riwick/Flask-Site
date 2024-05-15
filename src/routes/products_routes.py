from flask import Blueprint, render_template, abort, request, redirect, flash

from src.routes.queries.products_queries import ProductQueries


products_router = Blueprint("products_router", __name__)


@products_router.route("/products/", methods=["GET"])
def get_all_products():
    products = ProductQueries.get_all_products_query()
    return render_template("products.html", products=products, title="Каталог")


@products_router.route("/products/<int:product_id>/", methods=["GET"])
def get_one_product(product_id: int):
    product = ProductQueries.get_one_product_query(product_id)
    if not product:
        abort(404)
    return render_template("products-detail.html", product=product, title=product.title)


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
    return render_template("add_product.html", title="Добавление продукта")


@products_router.route('/products/<int:product_id>/delete_product/', methods=["DELETE", "POST", "GET"])
def delete_product(product_id: int):
    detail, status = ProductQueries.delete_product_query(product_id)
    if status:
        flash(detail, category="success")
    else:
        flash(detail, category="error")

    return redirect("/products")
