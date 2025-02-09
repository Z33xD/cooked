const ingredientInput = document.getElementById("ingredient-input");
const suggestionsList = document.getElementById("suggestions");
const selectedIngredientsContainer = document.getElementById("selected-ingredients");
let selectedIngredients = [];

// Fetch suggestions from Spoonacular API
const fetchSuggestions = async (query) => {
    if (query.trim() === "") {
        suggestionsList.style.display = "none";
        return;
    }

    try {
        const apiKey = "b7d6f7bf16ab4deb8ea6120e727c3f6f";
        const response = await fetch(`https://api.spoonacular.com/food/ingredients/autocomplete?query=${query}&number=5&apiKey=${apiKey}`);
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

    const bubble = document.createElement("span");
    bubble.className = "ingredient-bubble badge bg-success text-white me-2 p-2";
    bubble.innerHTML = `${ingredient} <span class="remove-ingredient" style="cursor: pointer; font-weight:bold; margin-left:5px;">&times;</span>`;

    selectedIngredientsContainer.appendChild(bubble);
    ingredientInput.value = "";
};

// Handle removing ingredients via event delegation
selectedIngredientsContainer.addEventListener("click", function (event) {
    if (event.target.classList.contains("remove-ingredient")) {
        const ingredient = event.target.parentElement.textContent.trim().slice(0, -2);
        selectedIngredients = selectedIngredients.filter(item => item !== ingredient);
        event.target.parentElement.remove();
    }
});

// Prevent form submission when pressing Enter
document.getElementById("ingredient-search-form").addEventListener("submit", function (event) {
    event.preventDefault();
    const ingredient = ingredientInput.value.trim();
    if (ingredient) {
        addIngredient(ingredient);
    }
});

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
