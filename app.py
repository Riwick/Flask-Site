import os.path

from flask import Flask, render_template, send_from_directory
from flask_login import LoginManager
from flask_migrate import Migrate

from src.admin.main import admin_router
from src.users.main import user_router
from src.main_routes import main_router
from src.products.main import products_router
from src.users.users_utils import UserLogin, USER_UPLOAD_FOLDER

from src.database import db
from src.config import SECRET_KEY, DB_NAME, DB_PORT, DB_HOST, DB_PASS, DB_USER
from src.products.utils import PRODUCTS_UPLOAD_FOLDER

app = Flask(__name__, template_folder="src/templates/")


if not os.path.exists("src/products/static/images/products_images/"):  # создание папки для изображений продуктов
    os.mkdir("src/products/static/images/products_images/")

if not os.path.exists("src/users/static/images/users_images/"):  # создание папки для изображений пользователей
    os.mkdir("src/users/static/images/users_images/")


app.static_folder = "src/static"
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["PRODUCT_UPLOAD_FOLDER"] = PRODUCTS_UPLOAD_FOLDER
app.config["USER_UPLOAD_FOLDER"] = USER_UPLOAD_FOLDER
# app.permanent_session_lifetime = datetime.timedelta(days=10)  # Задание срока жизни сессии


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "route.login"
login_manager.login_message = "Войдите в аккаунт для доступа к закрытым страницам"
login_manager.login_message_category = "success"


db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(user_router, url_prefix="/users")
app.register_blueprint(main_router)
app.register_blueprint(products_router, url_prefix="/products")
app.register_blueprint(admin_router, url_prefix="/admin")


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


# @login_manager.unauthorized_handler
# def unauthorized():
#     flash("Войдите в аккаунт для доступа к закрытым страницам", category="success")
#     return redirect("/login")


if __name__ == '__main__':
    app.run(debug=True)
