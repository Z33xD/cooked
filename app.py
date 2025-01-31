from flask import Flask, render_template, request, jsonify
import requests

# Configure Application
app = Flask(__name__)


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


@app.route('/search_ingredients', methods=['POST'])   
def search_ingredients():
    return render_template('search_with_ingredients.html')


@app.route('/meal_planner')
def meal_planner():
    return render_template('meal_planner.html')


if __name__ == "__main__":
    app.run(debug=True)