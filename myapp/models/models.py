from . import db


class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Numeric(2, 1), nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    ingredients = relationship("Ingredient", secondary="recipe_ingredients")


class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    recipes = relationship("Recipe", secondary="recipe_ingredients")


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredients"
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), primary_key=True)
    ingredient_id = db.Column(
        db.Integer, db.ForeignKey("ingredients.id"), primary_key=True
    )
