// Reference to the input field and the container for selected ingredients
const ingredientInput = document.getElementById("ingredient-input");
const suggestionsList = document.getElementById("suggestions")
const selectedIngredientsContainer = document.getElementById("selected-ingredients");

// Store selected ingredients in an array
let selectedIngredients = [];

// Fetch suggestions from Spoonacular
const fetchSuggestions = async(query) => {
    if (query.trim() === "") {
        suggestionsList.style.display = "none";
        return;
    }

    try {
        const apiKey = "b7d6f7bf16ab4deb8ea6120e727c3f6f";
        const response = await fetch(`https://api.spoonacular.com/food/ingredients/autocomplete?query=${query}&number=5&apiKey=${apiKey}`);
        const suggestions = await response.json();

        // Populate dropdown
        displaySuggestions(suggestions);
    } catch (error) {
        console.error("Error fetching suggestions: ", (error));
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

        // Add click event to select suggestion
        listItem.addEventListener("click", () => {
            addIngredient(suggestion.name);
            suggestionsList.style.display = "none";
        });
        suggestionsList.appendChild(listItem);
    });
    suggestionsList.style.display = "block";
};

// Add ingredient and create bubble
const addIngredient = (ingredient) => {
    if (!selectedIngredients.includes(ingredient)) {
        selectedIngredients.push(ingredient);
        const bubble = document.createElement("div");
        bubble.className = "ingredient-bubble d-flex align-items-center bg-light text-dark rounder-pill px-3 py-1 m-1";
        bubble.innerHTML = `
            <span>${ingredient}</span>
            <button type="button" class="btn-close ms-2" aria-label="Remove"></button>
        `;

        // Add an event listener to the remove button
        bubble.querySelector(".btn-close").addEventListener("click", () => {
            // Remove from selectedIngredients array
            selectedIngredients = selectedIngredients.filter(item => item != ingredient);
            // Remove bubble from DOM
            selectedIngredientsContainer.removeChild(bubble);
        });
        selectedIngredientsContainer.appendChild(bubble);
    }
    ingredientInput.value = "";
}

// Event listener for input field
ingredientInput.addEventListener("input", (event) => {
    const query = event.target.value;
    fetchSuggestions(query);
});

// Hide suggestions when clicking outside
document.addEventListener("click", (event) => {
    if (!suggestionsList.contains(event.target) && event.target !== ingredientInput) {
        suggestionsList.style.display = "none";
    }
});

// Add ingredient on Enter or button click
ingredientInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter" && ingredientInput.value.trim() !== "") {
        event.preventDefault();
        const newIngredient = ingredientInput.value.trim();

        // To avoid duplicates
        if (!selectedIngredients.includes(newIngredient)) {
            selectedIngredients.push(newIngredient);
            const bubble = createIngredientBubble(newIngredient);
            selectedIngredientsContainer.appendChild(bubble);
        }

        // Clear input field
        ingredientInput.value = "";
    }
});