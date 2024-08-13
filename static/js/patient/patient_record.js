document.addEventListener("DOMContentLoaded", function() {
    // Add event listener to "Add Record" button
    document.getElementById("addRecordButton").addEventListener("click", function() {
        // Redirect user to the "choose_form" page
        window.location.href = "{% url 'choose_form' %}";
    });
});

