import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():  # param = config_class=Config
    app = Flask(__name__, template_folder="myapp/templates", static_folder="../static")
    # basedir = os.path.abspath(os.path.dirname(__file__))
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "sqlite:///recipes.db"  # + os.path.join(basedir, "recipes.db")  # /recipesDB"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .routes.routes import bp

    app.register_blueprint(bp)

    # Import and register your blueprints here
    # from .views import your_blueprint
    # app.register_blueprint(your_blueprint)
    return app
