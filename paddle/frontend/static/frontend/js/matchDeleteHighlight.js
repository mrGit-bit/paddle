document.addEventListener("DOMContentLoaded", function () {
    console.log("Document loaded. Initializing delete buttons...");

    // Select all delete buttons
    const deleteButtons = document.querySelectorAll("[id^='delete-button-']");

    deleteButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent immediate navigation

            console.log("Delete button clicked:", button.id);

            // Extract the match ID from the button's ID
            const matchId = button.id.replace("delete-button-", "");
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
                    const confirmDelete = confirm('Are you sure you want to delete this match?');

                    if (confirmDelete) {
                        console.log("User confirmed deletion for match:", matchId);
                        // Redirect to the delete URL
                        window.location.href = button.getAttribute("href");
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
});
