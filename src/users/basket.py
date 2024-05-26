from flask import Blueprint, render_template, flash, redirect
from flask_login import login_required, current_user

from src.caching import delete_all_basket_cache
from src.users.users_queries import UserBasketQueries
from src.users.users_utils import get_total_basket_sum

basket_router = Blueprint("basket_router", __name__)


@basket_router.route("/basket", methods=["GET"])
@login_required
def get_basket():
    basket = UserBasketQueries.get_basket_products_query(current_user.get_id())
    total_price = get_total_basket_sum(basket)
    return render_template("users/basket.html", basket=basket, total_price=total_price)


@basket_router.route(
    "/basket/<int:user_id>/<int:product_id>/delete", methods=["POST", "DELETE", "GET"]
)
@login_required
def delete_product_from_basket(user_id: int, product_id: int):
    detail, result = UserBasketQueries.delete_product_from_basket_query(user_id, product_id)
    if result:
        flash(detail, category="success")
        delete_all_basket_cache(user_id)
    else:
        flash(detail, category="error")

    return redirect("/users/basket")


@basket_router.route("/<int:product_id>/<int:user_id>/add_to_basket")
@login_required
def add_product_to_basket(product_id: int, user_id: int):
    detail, result = UserBasketQueries.add_product_to_basket_query(product_id, user_id)
    if result:
        flash(detail, category="success")
        delete_all_basket_cache(user_id)
    else:
        flash(detail, category="error")

    return redirect("/products")