import datetime

from flask import Flask, render_template, send_from_directory, url_for, redirect
from flask_login import LoginManager

from src.routes.user_routes import user_router
from src.routes.main_routes import main_router
from src.routes.products_routes import products_router
from src.user_utils import UserLogin, USER_UPLOAD_FOLDER

from src.database import db
from src.config import SECRET_KEY, DB_NAME, DB_PORT, DB_HOST, DB_PASS, DB_USER
from src.routes.utils import PRODUCTS_UPLOAD_FOLDER

app = Flask("Riwi_Site", template_folder="src/templates/")

app.static_folder = "src/static"
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["PRODUCT_UPLOAD_FOLDER"] = PRODUCTS_UPLOAD_FOLDER
app.config["USER_UPLOAD_FOLDER"] = USER_UPLOAD_FOLDER
app.permanent_session_lifetime = datetime.timedelta(days=10)  # Задание срока жизни сессии


login_manager = LoginManager()
login_manager.init_app(app)


db.init_app(app)

with app.app_context():
    db.create_all()


app.register_blueprint(user_router)
app.register_blueprint(main_router)
app.register_blueprint(products_router)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/page404.html", title="Страница не найдена"), 404


@app.route("/products-uploads/<filename>")
def uploaded_product_file(filename):
    return send_from_directory(app.config['PRODUCT_UPLOAD_FOLDER'],
                               filename)


@app.route("/user-uploads/<filename>")
def uploaded_user_file(filename):
    return send_from_directory(app.config['USER_UPLOAD_FOLDER'],
                               filename)


@login_manager.user_loader
def load_user(user_id: int):
    return UserLogin().get_user_from_db(user_id, db)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")


if __name__ == '__main__':
    app.run(debug=True)
