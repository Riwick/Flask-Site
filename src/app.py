from flask import Flask

from src.routes import app_route

app = Flask("Riwi Site", template_folder="src/templates/")
app.register_blueprint(app_route)

app.run(debug=True)
