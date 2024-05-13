from flask import Blueprint, render_template, request, flash, make_response

from src.routes.queries.main_queries import MainQueries


main_router = Blueprint("main_routes", __name__)


@main_router.route("/")
def index():
    res_obj = make_response(render_template("index.html", title="Главная страница"), 200)
    res_obj.headers["Content-type"] = "text/html"
    res_obj.headers["Server"] = "flasksite"
    return res_obj


@main_router.route("/about")
def about():
    return render_template("about.html", title="Про нас")


@main_router.route("/contacts", methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        phone_number = request.form["phone-number"]
        message = request.form["message"]

        detail, status = MainQueries.add_feedback(username, email, phone_number, message)
        if status:
            flash(detail, category="success")
        else:
            flash(detail, category="error")

    return render_template("contacts.html", title="Обратная связь")
