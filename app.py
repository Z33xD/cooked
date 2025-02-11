import os
import json
import requests
from flask import Flask, request, jsonify, render_template, url_for, redirect


# Configure Application
app = Flask(__name__)


# API Key for Spoonacular
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
if not SPOONACULAR_API_KEY:
    raise ValueError("❌ ERROR: Spoonacular API key is missing! Set SPOONACULAR_API_KEY as an environment variable.")


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/search_with_ingredients')
def search_with_ingredients():
    return render_template('search_with_ingredients.html')


# Function to fetch recipes based on user-selected ingredients
def get_recipes_based_on_ingredients(ingredients):
    api_url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "apiKey": os.getenv("SPOONACULAR_API_KEY"),
        "ingredients": ",".join(ingredients),
        "number": 5,
        "ranking": 1,  # Prioritize recipes with more matched ingredients
        "ignorePantry": True
    }

    print("Requesting recipes with ingredients:", params)  # Debugging

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        recipes = response.json()

        # Ensure usedIngredients and missedIngredients are included
        for recipe in recipes:
            recipe["usedIngredients"] = recipe.get("usedIngredients", [])
            recipe["missedIngredients"] = recipe.get("missedIngredients", [])

        print("API Response:", recipes)  # Debugging
        return recipes

    except requests.exceptions.RequestException as e:
        print("API Request Failed:", e)
        return []


@app.route('/search_ingredients', methods=['POST'])
def search_ingredients():
    user_ingredients = request.form.get("ingredients")  
    user_ingredient_list = [ing.strip().lower() for ing in user_ingredients.split(",")]

    response = requests.get(
        "https://api.spoonacular.com/recipes/findByIngredients",
        params={"ingredients": user_ingredients, "number": 5, "apiKey": SPOONACULAR_API_KEY},
    )

    if response.status_code != 200:
        return jsonify({"error": f"Failed to fetch recipes: {response.text}"}), response.status_code

    recipes = response.json()

    return render_template("search_results.html", recipes=recipes)


# Function to fetch recipes based on user-selected nutrition filters
def get_recipes_based_on_nutrition(filters):
    api_url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": os.getenv("SPOONACULAR_API_KEY"),
        "number": 5,
        "addRecipeNutrition": True  # Ensures nutrition info is included
    }

    # Add the filter constraints to API request
    for nutrient, value in filters.items():
        params[f"min{nutrient.capitalize()}"] = max(value - 10, 0)  # Lower bound
        params[f"max{nutrient.capitalize()}"] = value + 10  # Upper bound

    print("Requesting recipes with nutrition filters:", params)  # Debugging

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        recipes = []
        for recipe in data.get("results", []):
            nutrition = {nutrient["name"].lower(): nutrient["amount"] for nutrient in recipe.get("nutrition", {}).get("nutrients", [])}

            recipes.append({
                "title": recipe["title"],
                "image": recipe["image"],
                "calories": nutrition.get("calories", "N/A"),
                "protein": nutrition.get("protein", "N/A"),
                "fat": nutrition.get("fat", "N/A"),
                "carbs": nutrition.get("carbohydrates", "N/A")
            })

        print("API Response:", recipes)  # Debugging
        return recipes

    except requests.exceptions.RequestException as e:
        print("API Request Failed:", e)
        return []


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


@app.route('/get_api_key')
def get_api_key():
    return jsonify({"apiKey": os.getenv("SPOONACULAR_API_KEY")})



if __name__ == "__main__":
    app.run(debug=True)
