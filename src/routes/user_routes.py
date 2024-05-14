from flask import render_template, Blueprint, session, abort, request, flash, redirect
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from src.routes.queries.user_queries import UserQueries
from src.routes.utils import validate_user_register
from src.user_utils import UserLogin

user_router = Blueprint("route", __name__)


@user_router.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user, status = UserQueries.select_user_by_email(request.form["email"])
        print(user)
        if status:
            if user and check_password_hash(user.password, request.form["password"]):

                user_login = UserLogin().create(user)
                login_user(user_login)
                return redirect("/")

    return render_template("login.html", title="Вход")


@user_router.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        password_confirm = request.form["password-confirm"]

        detail, status = validate_user_register(username, password, password_confirm, email, phone)

        if status:
            hashed_password = generate_password_hash(password)
            db_detail, db_status = UserQueries.create_user(username, hashed_password, email, phone)

            if db_status:
                flash(db_detail, category="success")
                return redirect("/login")
            else:
                flash(db_detail, category="error")
        else:
            flash(detail, category="error")

    return render_template("register.html", title="Регистрация")


@user_router.route("/profile")
@login_required
def profile():
    return f"Страница профиля"


@user_router.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")
