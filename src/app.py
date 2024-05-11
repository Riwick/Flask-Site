from flask import Flask, render_template

from src.routes import app_route
from src.config import SECRET_KEY, DB_NAME, DB_PORT, DB_HOST, DB_PASS, DB_USER
from src.database import db

app = Flask("Riwi Site", template_folder="src/templates/")
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db.init_app(app)

with app.app_context():
    db.create_all()


app.register_blueprint(app_route)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/page404.html", title="Страница не найдена"), 404


if __name__ == '__main__':
    app.run(debug=True)
