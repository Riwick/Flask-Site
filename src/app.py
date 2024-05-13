from flask import Flask, render_template, send_from_directory

from src.routes.user_routes import app_router
from src.routes.main_routes import main_router
from src.routes.products_routes import products_router

from src.database import db
from src.config import SECRET_KEY, DB_NAME, DB_PORT, DB_HOST, DB_PASS, DB_USER
from src.routes.utils import UPLOAD_FOLDER

app = Flask("Riwi Site", template_folder="src/templates/")

app.static_folder = "src/static"
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db.init_app(app)

with app.app_context():
    db.create_all()


app.register_blueprint(app_router)
app.register_blueprint(main_router)
app.register_blueprint(products_router)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/page404.html", title="Страница не найдена"), 404


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug=True)
