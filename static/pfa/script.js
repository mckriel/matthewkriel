// static/pfa/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const dayDropDown = document.getElementById('id_day_of_week');
    const categoryButtons = document.querySelectorAll('.category-button');
    const selectedCategory = selectedCategoryGlobal; // Use a global variable

    // Function to update the selected button
    function updateSelectedButton(selected) {
        categoryButtons.forEach(button => {
            button.classList.remove('selected');
            if (button.dataset.category === selected) {
                button.classList.add('selected');
            }
        });
    }

    dayDropDown.addEventListener('change', function() {
        document.getElementById('filterForm').submit();
    });

    categoryButtons.forEach(button => {
        button.addEventListener('click', function() {
            const categoryInput = document.getElementById('id_category');
            categoryInput.value = button.dataset.category;
            document.getElementById('filterForm').submit();
        });
    });

    // Set the initial selected button based on the selectedCategory
    updateSelectedButton(selectedCategory || 'all');
});
