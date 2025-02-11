document.addEventListener("DOMContentLoaded", function () {
    function toggleSlider(checkboxId, sliderId, valueId) {
        const checkbox = document.getElementById(checkboxId);
        const slider = document.getElementById(sliderId);
        const valueDisplay = document.getElementById(valueId);

        if (!checkbox || !slider || !valueDisplay) {
            console.error(`Element not found - ${checkboxId}, ${sliderId}, or ${valueId}`);
            return;
        }

        checkbox.addEventListener("change", function () {
            slider.disabled = !checkbox.checked;
            slider.style.opacity = checkbox.checked ? "1" : "0.5";
        });

        slider.addEventListener("input", function () {
            valueDisplay.textContent = slider.value;
        });
    }

    toggleSlider("calories_enabled", "calories", "calories_value");
    toggleSlider("protein_enabled", "protein", "protein_value");
    toggleSlider("fat_enabled", "fat", "fat_value");
    toggleSlider("carbs_enabled", "carbs", "carbs_value");

    document.getElementById("nutrition-search-form")?.addEventListener("submit", function () {
        document.querySelectorAll("input[type=range]").forEach(slider => {
            if (!slider.disabled) {
                slider.removeAttribute("disabled");
            }
        });
    });
});
