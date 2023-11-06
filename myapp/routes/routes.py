from flask import Blueprint, render_template, request

from myapp.models.query import *

# You can create a Blueprint and import it in __init__.py if you prefer
bp = Blueprint("main", __name__, template_folder="../templates")


@bp.route("/")
def home():
    return render_template("index.html")


@bp.route("/search", methods=["POST"])
def search():
    print("search hit")
    # Get lists of included and excluded ingredients
    include_ingredients = request.form.getlist("include-ingredient")
    exclude_ingredients = request.form.getlist("exclude-ingredient")
    recipes = [
        {"title": "Recipe 1", "link": "/recipe1"},
        {"title": "Recipe 2", "link": "/recipe2"},
        {"title": "Recipe 3", "link": "/recipe3"},
    ]
    print("oopsies")  #
    recipes = get_recipes_without_ingredients(exclude_ingredients)
    # For demonstration purposes, print the selected ingredients to console
    print("Included Ingredients:", include_ingredients)
    print("Excluded Ingredients:", exclude_ingredients)

    # Here you would typically query your database based on the selected ingredients
    # and return the results to the user.
    # For this example, we'll just return a simple text response.
    print("Recipes searched! Check server logs for selected ingredients.")
    return render_template("search_results.html", recipes=recipes)


def init_app(app):
    app.register_blueprint(bp)
