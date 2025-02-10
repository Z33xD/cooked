from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests

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

@app.route('/search_nutrition')
def search_nutrition():
    return render_template('search_with_nutrition.html')

@app.route('/meal_planner')
def meal_planner():
    return render_template('meal_planner.html')

@app.route('/search_ingredients', methods=['POST'])
def search_ingredients():
    user_ingredients = request.form.get("ingredients")  # Get ingredients from the hidden input
    user_ingredient_list = [ing.strip().lower() for ing in user_ingredients.split(",")]

    # Fetch recipes from spoonacular
    response = requests.get(f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={user_ingredients}&number=5&apiKey={SPOONACULAR_API_KEY}")

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch recipes"}), 500
    
    recipes = response.json()

    processed_recipes = []
    for recipe in recipes:
        recipe_ingredients = [ing["name"].lower() for ing in recipe["missedIngredients"] + recipe["usedIngredients"]]

        matched = [ing for ing in recipe_ingredients if ing in user_ingredient_list]
        missing = [ing for ing in recipe_ingredients if ing not in user_ingredient_list]

        processed_recipes.append({
            "title": recipe["title"],
            "image": recipe["image"],
            "matched_ingredients": matched,
            "missing_ingredients": missing
        })

    return render_template("search_results.html", recipes=processed_recipes)

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
