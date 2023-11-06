# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="app/templates")
    app.config.from_object(config_class)

    db.init_app(app)

    # Import and register your blueprints here
    # from .views import your_blueprint
    # app.register_blueprint(your_blueprint)

    return app


# config/config.py
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:password@localhost/recipesDB"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # other configurations...


# models/models.py
from . import db


class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    # other fields...


# app.py
from your_package import create_app, db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
