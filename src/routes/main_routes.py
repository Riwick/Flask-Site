from flask import Blueprint, render_template, request, flash, make_response, session

from src.routes.queries.main_queries import MainQueries


main_router = Blueprint("main_routes", __name__)


@main_router.route("/")
def index():
    res_obj = make_response(render_template("index.html", title="Главная страница"), 200)
    res_obj.headers["Content-type"] = "text/html"
    res_obj.headers["Server"] = "flasksite"
    res_obj.set_cookie("I_fucked_your_mom", "True", 10)
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


@main_router.route("/test-route/")
def test_route():
    if "visits" in session:
        session["visits"] = session.get("visits") + 1
    else:
        session["visits"] = 1
    return f"<h1>Main Page</h1><p>Количество просмотров: {session['visits']}</p>"


data = [1, 2, 3, 4]
@main_router.route("/session/")
def session_route():
    session.permanent = True  # Параметр, необходимый для сохранения сессии после закрытия браузера
    if "data" not in session:
        session["data"] = data
    else:
        session["data"][1] += 1
        session.modified = True
    return f"session['data']: {session['data']}"
