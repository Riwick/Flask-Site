from flask import render_template, Blueprint, session, abort, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from src.routes.queries.user_queries import UserQueries
from src.routes.utils import validate_user_register

app_router = Blueprint("route", __name__)


@app_router.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html", title="Вход")


@app_router.route("/register", methods=["GET", "POST"])
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


@app_router.route("/profile/<email>")
def profile(email):
    if "userLogged" not in session or session["userLogged"] != email:
        abort(401)

    return f"Пользователь: {email}"

