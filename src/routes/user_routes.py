from flask import render_template, Blueprint, session, abort

app_router = Blueprint("route", __name__)


@app_router.route("/login", methods=["GET", "POST"])
def login():
    # if "userLogged" in session:
    #     return redirect(url_for("route.profile", email=session["userLogged"]))
    #
    # if request.method == "POST" and request.form["email"] == "Riwi@gmail.com" and request.form["password"] == "123":
    #     if request.form["remember-me"]:
    #         session["userLogged"] = request.form["email"]
    #         return redirect(url_for("route.profile", email=request.form["email"]))
    #     else:
    #         return redirect("/")
    return render_template("login.html", title="Авторизация")


@app_router.route("/profile/<email>")
def profile(email):
    if "userLogged" not in session or session["userLogged"] != email:
        abort(401)

    return f"Пользователь: {email}"

