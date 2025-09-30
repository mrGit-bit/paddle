// path: paddle/frontend/static/frontend/js/matchDeleteHighlight.js

document.addEventListener("DOMContentLoaded", function () {
    console.log("Document loaded. Initializing delete buttons...");

    // Select all delete buttons
    const deleteButtons = document.querySelectorAll(".delete-button");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent immediate navigation

            console.log("Delete button clicked:", button.id);

            // Extract the match ID from the button's ID
            const matchId = button.getAttribute("data-match-id");
            const matchCard = document.getElementById(`match-card-${matchId}`);

            if (matchCard) {
                // Log original classes
                console.log("Original classes:", matchCard.className);

                // Store original background classes
                const originalClasses = matchCard.className;

                // Change background color to indicate deletion
                matchCard.classList.add("text-bg-secondary");
                console.log("Background changed for match:", matchId);

                // Use setTimeout to allow DOM repaint before the confirm dialog
                
                setTimeout(() => {
                    const confirmDelete = confirm('Estas seguro?');

                    if (confirmDelete) {
                        console.log("User confirmed deletion for match:", matchId);
                        // Send a DELETE request to the API view match_view
                        fetch(`/matches/`, {
                            method: "DELETE",
                            headers: {
                                "Content-Type": "application/json",
                                "X-CSRFToken": getCSRFToken()
                            },
                            body: JSON.stringify({ match_id: matchId })
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.message) {
                                console.log("Match deleted successfully:", matchId);
                                window.location.href = "/matches/";  // Redirect for PRG pattern
                            } else {
                                alert("Error al eliminar el partido: " + data.error);
                                matchCard.classList.remove("text-bg-secondary"); // Restore original style
                            }
                        })
                        .catch(error => {
                            console.error("Error deleting match:", error);
                            alert("An error occurred while deleting the match.");
                            matchCard.className = originalClasses; // Restore original style
                        });
                    } else {
                        console.log("User canceled deletion for match:", matchId);
                        // Restore original background color if canceled
                        matchCard.className = originalClasses;
                        console.log("Background restored for match:", matchId);
                    }
                }, 10); // Short delay to allow DOM to repaint
                
            } else {
                console.log("Match card not found for match:", matchId);
            }
        });
    });
    // Function to get CSRF token from cookies
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            cookies.forEach(cookie => {
                const trimmed = cookie.trim();
                if (trimmed.startsWith("csrftoken=")) {
                    cookieValue = trimmed.substring("csrftoken=".length);
                }
            });
        }
        return cookieValue;
    }
});
