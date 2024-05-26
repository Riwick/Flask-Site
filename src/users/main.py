from flask import render_template, Blueprint, request, flash, redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from src.users.users_queries import UserQueries, UserBasketQueries
from src.users.users_utils import UserLogin, get_total_basket_sum
from src.users.forms import LoginForm, RegisterForm
from src.caching import (
    delete_all_user_cache,
    delete_all_user_cache_without_id,
    delete_all_basket_cache
)
from src.users.favorites import favorites_router
from src.users.basket import basket_router

user_router = Blueprint(
    "users_router", __name__, template_folder="templates", static_folder="static"
)

user_router.register_blueprint(favorites_router)
user_router.register_blueprint(basket_router)


@user_router.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/users/profile")

    form = LoginForm()
    if form.validate_on_submit():
        user, status = UserQueries.select_user_by_email_query(form.email.data)

        if status and check_password_hash(user.password, form.password.data):
            user_login = UserLogin().create(user)
            rem_me = form.remember.data
            login_user(user_login, remember=rem_me)
            return redirect(request.args.get("next") or "/")

        else:
            flash("Неверные email или пароль", category="error")

    return render_template("users/login.html", title="Вход", form=form)


@user_router.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/users/profile")

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        db_detail, db_status = UserQueries.create_user_query(
            form.username.data, hashed_password, form.email.data, form.phone.data
        )
        if db_status:
            flash(db_detail, category="success")
            delete_all_user_cache_without_id()
            return redirect("/users/login")
        else:
            flash(db_detail, category="error")

    return render_template("users/register.html", title="Регистрация", form=form)


@user_router.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        detail, status = UserQueries.update_profile_query(
            request.files.get("image"),
            request.form.get("name"),
            request.form.get("surname"),
            request.form.get("username"),
            request.form.get("address"),
            request.form.get("additional_address"),
            request.form.get("country"),
            current_user.get_id(),
        )
        if status:
            flash(detail, category="success")
            delete_all_user_cache(current_user.get_id())
        else:
            flash(detail, category="error")

    return render_template(
        "users/profile.html", title=f"Профиль {current_user.get_username()}"
    )


@user_router.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/users/login")
