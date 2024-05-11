from flask import Flask

from src.routes import app_route
from src.config import SECRET_KEY

app = Flask("Riwi Site", template_folder="src/templates/")
app.config["SECRET_KEY"] = SECRET_KEY

app.register_blueprint(app_route)

if __name__ == '__main__':
    app.run(debug=True)
