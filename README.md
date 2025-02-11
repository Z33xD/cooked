# cooked
#### Video Demo:  [cooked Showcase](https://www.youtube.com/watch?v=5hqCqHvKo3w)
#### Description:
cooked is a Flask based web application that shows you recipes with your inputs. It uses the Spoonacular API ([Spoonacular](https://spoonacular.com/food-api)), and uses some of its functionalities like [Searching with Nutrition](https://spoonacular.com/food-api/docs#Search-Recipes-by-Nutrients) and [Searching with Ingredients](https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients) that do just about that.
The primary aim of cooked is to make cooking more convenient, reduce food waste, and help users maintain their dietary goals without the hassle of manually searching through endless recipe options. Whether someone is trying to use up ingredients already available in their kitchen or looking for meal ideas that fit their nutritional intake, cooked provides an efficient and user-friendly solution.

## Searching with Ingredients
One of the core functionalities of cooked is ingredient-based search. This feature enables users to input a list of ingredients into a search bar, which then provides auto-complete suggestions. Once the user selects their desired ingredients, the system processes the input and searches for recipes that incorporate those ingredients. The search results display relevant recipes along with a breakdown of matched and missing ingredients.
The matched ingredients highlight which items from the user's input are already present in the suggested recipes, while the missing ingredients indicate additional components required to complete the dish. This provides valuable insight for users who may want to quickly check if they can make a recipe without needing to buy additional groceries.
### Use Case & Vision
The inspiration behind this feature was to help people make better use of the ingredients they already have at home. Many people often find themselves with leftover or unused ingredients in their kitchens but struggle to decide what to cook with them. By allowing users to quickly search for recipes using the ingredients they have on hand, cooked helps minimize food waste while encouraging creativity in meal preparation.
For example, a user might have eggs, tomatoes, and spinach but is not sure what they can make with those ingredients. By entering them into cooked, they can find recipe suggestions that incorporate these ingredients, potentially discovering new dishes they had not considered before. Additionally, by seeing the missing ingredients, users can decide whether they want to purchase the additional items or modify the recipe based on what they have.

## Searching with Nutrition
In addition to ingredient-based searches, cooked also offers a nutrition-based search feature. This allows users to filter recipes based on their nutritional needs by selecting from four key nutrient categories:
- Calories
- Proteins
- Fats
- Carbohydrates
The user can toggle checkboxes to indicate which of these nutrients they want to focus on. At least one category must be selected before proceeding. Once a category is enabled, a slider control appears, allowing the user to specify their desired intake range for that nutrient.
### How It Works
After selecting a nutrient and setting a preferred intake value, cooked retrieves recipes that match the input criteria. Instead of strictly enforcing an exact match (which could severely limit results), the application applies a tolerance of ±10 units. For example, if a user sets a protein intake of 25g, the system will return recipes with protein values ranging from 15g to 35g. This approach ensures flexibility while still maintaining relevance to the user’s nutritional goals.
### Use Case & Vision
The motivation behind this feature was to help users make informed dietary choices, whether they are meal planning, managing a specific diet, or simply aiming to eat healthier. Many people struggle with finding meals that align with their fitness or dietary goals, and manually checking the nutritional breakdown of different recipes can be time-consuming. cooked simplifies this process by filtering recipes that match their desired intake.
This functionality is especially useful for individuals following specific dietary plans such as:
- Bodybuilders or athletes who need high-protein meals
- People on weight-loss diets looking for low-calorie options
- Individuals managing medical conditions (e.g., diabetes, keto diet, low-carb diets)
- For instance, if a user is trying to reduce calorie intake but still wants satisfying meals, they can set a lower calorie range and explore recipes that fit within those limits. Similarly, if someone is on a high-protein diet, they can easily discover meals that support their fitness goals.

## Future Improvements & Enhancements
1. While cooked already provides valuable functionality, there are several areas where it could be further improved:
2. Expanded Ingredient Filters -- Adding filters such as dietary restrictions (vegetarian, vegan, gluten-free) or allergies (nut-free, dairy-free) could make the ingredient search even more useful.
3. User Accounts & Meal Planning -- Allowing users to create accounts and save favorite recipes, track daily nutrition, and generate weekly meal plans would enhance the overall experience.
4. More Advanced Nutrient Customization -- Adding more nutrient categories (e.g., vitamins, minerals) and letting users set multiple constraints at once would provide greater control over meal selection.
5. Recipe Ratings & Reviews -- Implementing a user rating system where people can leave feedback on recipes could help improve search results based on real user experiences.
