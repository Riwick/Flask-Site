from flask import render_template, Blueprint, request, flash, session, redirect, url_for, abort

from src.database import db


app_route = Blueprint("route", __name__)


@app_route.route("/")
def index():
    return render_template("index.html", title="Главная страница")


@app_route.route("/about")
def about():
    return render_template("about.html", title="Про нас")


@app_route.route("/contacts", methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        if request.form["username"] and request.form["email"] and request.form["message"]:
            flash("Сообщение отправлено", category="success")
        else:
            flash("Ошибка отправки сообщения", category="error")
        print(request.form)

    return render_template("contacts.html", title="Обратная связь")


@app_route.route("/login", methods=["GET", "POST"])
def login():
    if "userLogged" in session:
        return redirect(url_for("route.profile", email=session["userLogged"]))

    if request.method == "POST" and request.form["email"] == "Riwi@gmail.com" and request.form["password"] == "123":
        if request.form["remember-me"]:
            session["userLogged"] = request.form["email"]
            return redirect(url_for("route.profile", email=request.form["email"]))
        else:
            return redirect("/")
    return render_template("login.html", title="Авторизация")


@app_route.route("/profile/<email>")
def profile(email):
    if "userLogged" not in session or session["userLogged"] != email:
        abort(401)

    return f"Пользователь: {email}"
