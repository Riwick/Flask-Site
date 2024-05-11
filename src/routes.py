from flask import render_template, Blueprint, request, flash, get_flashed_messages


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
