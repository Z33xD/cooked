from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import requests
import os


# Configure Application
app = Flask(__name__)


# API Key for Spoonacular
SPOONACULAR_API_KEY = "b7d6f7bf16ab4deb8ea6120e727c3f6f"


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/search_with_ingredients')
def search_with_ingredients():
    return render_template('search_with_ingredients.html')


@app.route('/search_ingredients', methods=['POST'])
def search_ingredients():
    user_ingredients = request.form.get("ingredients")  # Get ingredients from the hidden input
    user_ingredient_list = [ing.strip().lower() for ing in user_ingredients.split(",")]

    # Fetch recipes from Spoonacular
    response = requests.get(f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={user_ingredients}&number=5&apiKey={SPOONACULAR_API_KEY}")

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch recipes"}), 500

    recipes = response.json()

    processed_recipes = []
    for recipe in recipes:
        matched = [ing["name"].capitalize() for ing in recipe.get("usedIngredients", [])]  # Capitalize for better display
        missing = [ing["name"].capitalize() for ing in recipe.get("missedIngredients", [])]

        processed_recipes.append({
            "title": recipe["title"],
            "image": recipe["image"],
            "matched_ingredients": matched if matched else None,
            "missing_ingredients": missing if missing else None
        })

        # Debugging
        print(f"Recipe: {recipe['title']}")
        print(f"Matched Ingredients: {matched}")
        print(f"Missing Ingredients: {missing}")

    return render_template("search_results.html", recipes=processed_recipes)


# Function to fetch recipes based on user-selected nutrition filters
def get_recipes_based_on_nutrition(filters):
    url = "https://api.spoonacular.com/recipes/findByNutrients"
    params = {
        "apiKey": SPOONACULAR_API_KEY,  # Ensure this is set
        "number": 5
    }

    if "protein" in filters:
        params["minProtein"] = filters["protein"] - 5
        params["maxProtein"] = filters["protein"] + 5

    print("API Request Params:", params)

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("API Error:", response.status_code, response.text)
        return []  # Don't break the app

    return response.json()


@app.route("/search_nutrition", methods=["GET", "POST"])
def search_nutrition():
    if request.method == "POST":
        print("Raw Form Data:", request.form)  # Debugging

        filters = {}
        tolerance = 10  # +/-10 range

        if "calories" in request.form and "calories_enabled" in request.form:
            filters["calories"] = int(request.form["calories"])
        if "protein" in request.form and "protein_enabled" in request.form:
            filters["protein"] = int(request.form["protein"])
        if "fat" in request.form and "fat_enabled" in request.form:
            filters["fat"] = int(request.form["fat"])
        if "carbs" in request.form and "carbs_enabled" in request.form:
            filters["carbs"] = int(request.form["carbs"])

        print("Filters applied:", filters)  # Debugging

        if not filters:
            return render_template("search_results.html", recipes=[])
        recipes = get_recipes_based_on_nutrition(filters)

        return render_template("search_results.html", recipes=recipes)

    return render_template("search_with_nutrition.html")


# Route to fetch and display search results
@app.route('/search-results')
def search_results():
    ingredients = request.args.get("ingredients")
    if not ingredients:
        return redirect(url_for("search_with_ingredients"))  # If no ingredients, go back

    # Fetch recipes from Spoonacular
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=5&apiKey={SPOONACULAR_API_KEY}"
    response = requests.get(url)
    recipes = response.json()

    return render_template("search_results.html", recipes=recipes, ingredients=ingredients)


if __name__ == "__main__":
    app.run(debug=True)
