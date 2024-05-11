from flask import Blueprint, render_template, request, flash

main_router = Blueprint("main_routes", __name__)


@main_router.route("/")
def index():
    return render_template("index.html", title="Главная страница")


@main_router.route("/about")
def about():
    return render_template("about.html", title="Про нас")


@main_router.route("/contacts", methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        if request.form["username"] and request.form["email"] and request.form["message"]:
            flash("Сообщение отправлено", category="success")
        else:
            flash("Ошибка отправки сообщения", category="error")
        print(request.form)

    return render_template("contacts.html", title="Обратная связь")
