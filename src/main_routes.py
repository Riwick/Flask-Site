from flask import Blueprint, render_template, flash, make_response, session
from flask_login import login_required

from src.main_queries import MainQueries
from src.forms import FeedBackForm


main_router = Blueprint("main_router", __name__)


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
@login_required
def contacts():
    form = FeedBackForm()
    if form.validate_on_submit():
        detail, status = MainQueries.add_feedback_query(form.username.data, form.email.data,
                                                        form.phone.data, form.message.data)
        if status:
            flash(detail, category="success")
        else:
            flash(detail, category="error")

    return render_template("contacts.html", title="Обратная связь", form=form)


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
        session.modified = True  # Параметр, указывающий браузеру, что мы обновили данные в сессии
    return f"session['data']: {session['data']}"
