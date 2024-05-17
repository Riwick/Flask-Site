from flask import render_template, Blueprint, session, abort, request, flash, redirect
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash

from src.database import Basket
from src.routes.queries.user_queries import UserQueries
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
        pass
    return render_template("profile.html", title=f"Профиль {current_user.get_username()}")


@user_router.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@user_router.route("/basket")
@login_required
def get_basket():
    basket = UserQueries.get_basket_query(current_user.get_id())
    return render_template("basket.html", basket=basket)


@user_router.route("/basket/<int:product_id>/delete")
@login_required
def delete_product_from_basket():
    try:
        detail, result = UserQueries