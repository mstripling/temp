from sqlalchemy import bindparam, create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

# SQLAlchemy setup
engine = create_engine("sqlite:///recipes.db")
Session = sessionmaker(bind=engine)
session = Session()


def get_recipes_without_ingredients(excluded_ingredients):
    # Convert list of excluded ingredients to a set for faster lookup
    excluded_ingredients_set = set(excluded_ingredients)

    # SQL query to find recipes without the excluded ingredients
    sql = text(
        """
        SELECT r.id, r.name, r.url, r.rating
        FROM recipes r
        WHERE NOT EXISTS (
            SELECT 1
            FROM recipe_ingredients ri
            JOIN ingredients i ON ri.ingredient_id = i.id
            WHERE ri.recipe_id = r.id AND i.name IN :excluded_ingredients
        );
    """
    ).bindparams(bindparam("excluded_ingredients", expanding=True))
    print(sql, excluded_ingredients_set)

    # Execute query
    results = session.execute(
        sql, {"excluded_ingredients": list(excluded_ingredients_set)}
    ).fetchall()

    # Convert result to list of dictionaries
    recipes = [
        {"id": row[0], "name": row[1], "url": row[2], "rating": row[3]}
        for row in results
    ]

    return recipes


# Example usage
# excluded_ingredients = ["Eggs", "Bacon"]
# recipes = get_recipes_without_ingredients(excluded_ingredients)
# print(recipes)


def insert_recipe(name, url, ingredients):
    try:
        # Insert the recipe
        insert_recipe_sql = text("INSERT INTO recipes (name, url) VALUES (:name, :url)")
        result = session.execute(insert_recipe_sql, {"name": name, "url": url})
        recipe_id = result.lastrowid

        # For each ingredient, insert it if it doesn't exist and associate it with the recipe
        for ingredient in ingredients:
            # Check if the ingredient already exists
            check_ingredient_sql = text("SELECT id FROM ingredients WHERE name = :name")
            result = session.execute(check_ingredient_sql, {"name": ingredient})
            row = result.fetchone()

            if row:
                ingredient_id = row[0]
            else:
                # Insert the ingredient if it doesn't exist
                insert_ingredient_sql = text(
                    "INSERT INTO ingredients (name) VALUES (:name)"
                )
                result = session.execute(insert_ingredient_sql, {"name": ingredient})
                ingredient_id = result.lastrowid

            # Associate the ingredient with the recipe
            associate_recipe_ingredient_sql = text(
                "INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (:recipe_id, :ingredient_id)"
            )
            session.execute(
                associate_recipe_ingredient_sql,
                {"recipe_id": recipe_id, "ingredient_id": ingredient_id},
            )

        # Commit the transaction
        session.commit()
        print("Recipe inserted successfully!")

    except IntegrityError as e:
        # Handle integrity errors, e.g., duplicate entries
        session.rollback()
        print("Error inserting recipe:", str(e))

    except Exception as e:
        # Handle other errors
        session.rollback()
        print("Error:", str(e))


# Example usage
# name = "Chicken Tacos"
# url = "http://example.com/chicken-tacos"
# ingredients = ["Chicken", "Taco Shells", "Cheese"]
# insert_recipe(name, url, ingredients)
