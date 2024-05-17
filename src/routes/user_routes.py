from flask import render_template, Blueprint, session, abort, request, flash, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from src.routes.queries.user_queries import UserQueries
from src.routes.utils import get_total_basket_sum
from src.user_utils import UserLogin, validate_user_register

user_router = Blueprint("route", __name__)


@user_router.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/profile")
    if request.method == "POST":
        user, status = UserQueries.select_user_by_email_query(request.form["email"])
        if status and check_password_hash(user.password, request.form["password"]):
            user_login = UserLogin().create(user)
            rem_me = True if request.form.get("remember") else False
            login_user(user_login, remember=rem_me)
            return redirect(request.args.get("next") or "/")
        else:
            flash("Неверные email или пароль", category="error")

    return render_template("login.html", title="Вход")


@user_router.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/profile")

    if request.method == "POST":
        detail, status = validate_user_register(request.form["username"],  request.form["password"],
                                                request.form["password-confirm"], request.form["email"],
                                                request.form["phone"])
        if status:
            hashed_password = generate_password_hash(request.form["password"])
            db_detail, db_status = UserQueries.create_user_query(request.form["username"], hashed_password,
                                                                 request.form["email"],
                                                                 request.form["phone"])
            if db_status:
                flash(db_detail, category="success")
                return redirect("/login")
            else:
                flash(db_detail, category="error")
        else:
            flash(detail, category="error")

    return render_template("register.html", title="Регистрация")


@user_router.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        detail, status = UserQueries.update_profile_query(request.files.get("image"),  request.form.get("name"),
                                                          request.form.get("surname"), request.form.get("username"),
                                                          request.form.get("address"),
                                                          request.form.get("additional_address"),
                                                          request.form.get("country"), current_user.get_id())
        if status:
            flash(detail, category="success")
        else:
            flash(detail, category="error")

    return render_template("profile.html", title=f"Профиль {current_user.get_username()}")


@user_router.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@user_router.route("/basket", methods=["GET"])
@login_required
def get_basket():
    basket = UserQueries.get_basket_products_query(current_user.get_id())
    total_price = get_total_basket_sum(basket)
    return render_template("basket.html", basket=basket, total_price=total_price)


@user_router.route("/basket/<int:user_id>/<int:product_id>/delete", methods=["POST", "DELETE", "GET"])
@login_required
def delete_product_from_basket(user_id: int, product_id: int):
    detail, result = UserQueries.delete_product_from_basket_query(user_id, product_id)
    if result:
        flash(detail, category="success")
    else:
        flash(detail, category="error")

    return redirect("/basket")


@user_router.route("/product/<int:product_id>/<int:user_id>/add_to_basket")
@login_required
def add_product_to_basket(product_id: int, user_id: int):
    detail, result = UserQueries.add_product_to_basket_query(product_id, user_id)
    if result:
        flash(detail, category="success")
    else:
        flash(detail, category="error")

    return redirect("/products")
