from flask import Blueprint, render_template, flash, redirect
from flask_login import login_required, current_user

from src.caching import delete_all_basket_cache
from src.users.users_queries import UserFavoritesQuery
from src.users.users_utils import get_total_basket_sum

favorites_router = Blueprint("favorites_router", __name__)


@favorites_router.route("/favorites", methods=["GET"])
@login_required
def get_basket():
    basket = UserFavoritesQuery.get_favorites_products_query(current_user.get_id())
    total_price = get_total_basket_sum(basket)
    return render_template("users/basket.html", basket=basket, total_price=total_price)


@favorites_router.route(
    "/favorites/<int:user_id>/<int:product_id>/delete", methods=["POST", "DELETE", "GET"]
)
@login_required
def delete_product_from_basket(user_id: int, product_id: int):
    detail, result = UserFavoritesQuery.delete_product_from_favorites_query(user_id, product_id)
    if result:
        flash(detail, category="success")
        delete_all_basket_cache(user_id)
    else:
        flash(detail, category="error")

    return redirect("/users/favorites")


@favorites_router.route("/<int:product_id>/<int:user_id>/add_to_favorites")
@login_required
def add_product_to_basket(product_id: int, user_id: int):
    detail, result = UserFavoritesQuery.add_product_to_favorites_query(product_id, user_id)
    if result:
        flash(detail, category="success")
        delete_all_basket_cache(user_id)
    else:
        flash(detail, category="error")

    return redirect("/products")
