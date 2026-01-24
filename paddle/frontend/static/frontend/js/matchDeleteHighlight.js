// absolute path: /workspaces/paddle/paddle/frontend/static/frontend/js/matchDeleteHighlight.js

document.addEventListener("DOMContentLoaded", function () {
  console.log("Document loaded. Initializing delete buttons...");

  const deleteButtons = document.querySelectorAll(".delete-button");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", function (event) {
      event.preventDefault(); // We will submit manually after confirm

      const matchId = button.getAttribute("data-match-id");
      const matchCard = document.getElementById(`match-card-${matchId}`);

      if (!matchCard) {
        console.log("Match card not found for match:", matchId);
        return;
      }

      const originalClasses = matchCard.className;

      // Highlight
      matchCard.classList.add("text-bg-secondary");

      // Allow repaint before confirm dialog
      setTimeout(() => {
        const confirmDelete = confirm("Estas seguro?");

        if (!confirmDelete) {
          // Restore if canceled
          matchCard.className = originalClasses;
          return;
        }

        // Submit the closest delete form (POST -> redirect -> messages)
        const form = button.closest("form");
        if (!form) {
          console.log("Delete form not found for match:", matchId);
          matchCard.className = originalClasses;
          return;
        }

        form.submit();
      }, 10);
    });
  });
});
