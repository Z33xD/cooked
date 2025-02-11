const ingredientInput = document.getElementById("ingredient-input");
const suggestionsList = document.getElementById("suggestions");
const selectedIngredientsContainer = document.getElementById("selected-ingredients");
const hiddenIngredientsInput = document.getElementById("hidden-ingredients");
let selectedIngredients = [];
let SPOONACULAR_API_KEY = ""; // Will be fetched dynamically

// Fetch the API key from the backend
const fetchApiKey = async () => {
    try {
        const response = await fetch("/get_api_key");
        const data = await response.json();
        SPOONACULAR_API_KEY = data.apiKey;
    } catch (error) {
        console.error("Error fetching API key: ", error);
    }
};

// Fetch ingredient suggestions from Spoonacular API
const fetchSuggestions = async (query) => {
    if (query.trim() === "") {
        suggestionsList.style.display = "none";
        return;
    }

    if (!SPOONACULAR_API_KEY) {
        console.error("API key is missing!");
        return;
    }

    try {
        const response = await fetch(`https://api.spoonacular.com/food/ingredients/autocomplete?query=${query}&number=5&apiKey=${SPOONACULAR_API_KEY}`);
        const suggestions = await response.json();
        displaySuggestions(suggestions);
    } catch (error) {
        console.error("Error fetching suggestions: ", error);
    }
};

// Display dropdown suggestions
const displaySuggestions = (suggestions) => {
    suggestionsList.innerHTML = "";

    if (suggestions.length === 0) {
        suggestionsList.style.display = "none";
        return;
    }

    suggestions.forEach((suggestion) => {
        const listItem = document.createElement("li");
        listItem.className = "list-group-item list-group-item-action";
        listItem.textContent = suggestion.name;

        listItem.addEventListener("click", () => {
            addIngredient(suggestion.name);
            suggestionsList.style.display = "none";
        });

        suggestionsList.appendChild(listItem);
    });

    suggestionsList.style.display = "block";
};

// Add ingredient and create a bubble
const addIngredient = (ingredient) => {
    if (selectedIngredients.includes(ingredient)) {
        ingredientInput.value = "";
        return;
    }

    selectedIngredients.push(ingredient);
    updateHiddenInput();

    const bubble = document.createElement("span");
    bubble.className = "ingredient-bubble badge bg-success text-white me-2 p-2";
    bubble.innerHTML = `${ingredient} <span class="remove-ingredient" style="cursor: pointer; font-weight:bold; margin-left:5px;">&times;</span>`;

    selectedIngredientsContainer.appendChild(bubble);
    ingredientInput.value = "";
};

// Update the hidden input field with selected ingredients
const updateHiddenInput = () => {
    hiddenIngredientsInput.value = selectedIngredients.join(",");
};

// Handle removing ingredients via event delegation
selectedIngredientsContainer.addEventListener("click", function (event) {
    if (event.target.classList.contains("remove-ingredient")) {
        const ingredient = event.target.parentElement.textContent.trim().slice(0, -2);
        selectedIngredients = selectedIngredients.filter(item => item !== ingredient);
        updateHiddenInput();
        event.target.parentElement.remove();
    }
});

// Fetch API key when the page loads
fetchApiKey();

// Fetch suggestions as user types
ingredientInput.addEventListener("input", (event) => {
    fetchSuggestions(event.target.value);
});

// Hide suggestions when clicking outside
document.addEventListener("click", (event) => {
    if (!suggestionsList.contains(event.target) && event.target !== ingredientInput) {
        suggestionsList.style.display = "none";
    }
});
