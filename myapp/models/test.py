from sqlalchemy.sql import text


def gen_sql(name, url, ingredients):
    # Escape single quotes in the string values
    name = name.replace("'", "''")
    url = url.replace("'", "''")
    ingredients = [ingredient.replace("'", "''") for ingredient in ingredients]

    # Generate SQL for inserting the recipe
    recipe_sql = f"INSERT INTO recipes (name, url) VALUES ('{name}', '{url}');"
    print(recipe_sql)

    for ingredient in ingredients:
        # Generate SQL for inserting the ingredient if it doesn't exist
        ingredient_sql = (
            f"INSERT IGNORE INTO ingredients (name) VALUES ('{ingredient}');"
        )
        print(ingredient_sql)

        # Generate SQL for associating the recipe with the ingredient
        association_sql = f"""
        INSERT INTO recipe_ingredients (recipe_id, ingredient_id) 
        VALUES (
            (SELECT id FROM recipes WHERE name = '{name}'), 
            (SELECT id FROM ingredients WHERE name = '{ingredient}')
        );
        """
        print(association_sql)


gen_sql("chicken tacos", "chicken-tacos.com", ["chicken", "dairy"])
gen_sql("bacon and eggs", "bacon-and-eggs.com", ["pork", "eggs"])
gen_sql("beef and rice", "beef-and-rice.com", ["beef"])

# Example usage
# name = "Chicken Tacos"
# url = "http://example.com/chicken-tacos"
# ingredients = ["Chicken", "Taco Shells", "Cheese"]
# gen_sql(name, url, ingredients)
