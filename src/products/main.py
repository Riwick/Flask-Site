from flask import Blueprint, render_template, abort, request
from flask_login import current_user
from flask_paginate import get_page_parameter

from src.products.products_queries import ProductQueries
from src.users.users_queries import UserBasketQueries, UserFavoritesQuery
from src.products.utils import get_pagination
from src.utils import get_paginated_staff, PER_PAGE

products_router = Blueprint(
    "products_router", __name__, template_folder="templates", static_folder="static"
)


@products_router.route("/", methods=["GET"])
def get_all_products():

    category = request.args.get("category")

    if category:
        products = ProductQueries.get_products_by_category(category)
    else:
        products = ProductQueries.get_all_products_query()

    baskets = UserBasketQueries.get_basket_query(current_user.get_id())
    categories = ProductQueries.get_all_categories()

    page = request.args.get(get_page_parameter(), type=int, default=1)
    paginated_products = get_paginated_staff(
        page=page, staff=products, per_page=PER_PAGE
    )

    return render_template(
        "products/products.html",
        products=paginated_products,
        title="Каталог",
        pagination=get_pagination(page=page, per_page=PER_PAGE, total=products),
        baskets=baskets,
        categories=categories,
    )


@products_router.route("/<int:product_id>/", methods=["GET"])
def get_one_product(product_id: int):
    product = ProductQueries.get_one_product_query(product_id)
    if not product:
        abort(404)
    return render_template(
        "products/products-detail.html", product=product, title=product.title
    )
