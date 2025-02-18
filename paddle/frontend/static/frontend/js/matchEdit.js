document.addEventListener("DOMContentLoaded", function () {
  console.log("Document loaded. Initializing edit buttons...");

  const currentUser = document.getElementById("team1_player1").value; // The logged-in user
  const matchForm = document.getElementById("add-edit-match-form");
  const submitButton = matchForm.querySelector("button[type='submit']");
  let cancelButton = null;

  // Select all edit buttons
  const editButtons = document.querySelectorAll("[id^='edit-button-']");

  editButtons.forEach((button) => {
    button.addEventListener("click", function (event) {
      event.preventDefault();
      console.log("Edit button clicked:", button.id);

      // Extract match ID and match data
      const matchId = button.dataset.matchId;
      const matchCard = document.getElementById(`match-card-${matchId}`);

      if (matchCard && matchForm) {
        let players = {
          team1_player1: matchCard.dataset.team1Player1,
          team1_player2: matchCard.dataset.team1Player2,
          team2_player1: matchCard.dataset.team2Player1,
          team2_player2: matchCard.dataset.team2Player2,
        };

        console.log("Loaded match data:", players);

        // Fill the form with the existing match data
        document.getElementById("team1_player1").value = players.team1_player1;
        document.getElementById("team1_player2").value = players.team1_player2;
        document.getElementById("team2_player1").value = players.team2_player1;
        document.getElementById("team2_player2").value = players.team2_player2;

        // Label the user field as "You" and disable it
        ["team1_player1", "team1_player2", "team2_player1", "team2_player2"].forEach((key) => {
          const inputField = document.getElementById(key);
          const label = document.querySelector(`label[for='${key}']`);

          if (players[key]?.trim().toLowerCase() === currentUser.trim().toLowerCase()) {
            inputField.readOnly = true; // Keep field visible but read-only
            inputField.disabled = true; // This field shall not be submitted
            label.textContent = "You";

            // Create a hidden input to allow submitting the disabled value
            let hiddenInput = document.getElementById(`hidden-${key}`);
            if (!hiddenInput) {
              hiddenInput = document.createElement("input");
              hiddenInput.type = "hidden";
              hiddenInput.id = `hidden-${key}`;
              hiddenInput.name = key;
              matchForm.appendChild(hiddenInput);
            }
            hiddenInput.value = players[key]; // Assign value to hidden input

          } else {
            inputField.readOnly = false;
            inputField.disabled = false;
            label.textContent = "Player";
          }
        });

        
        // Keep the original winning team
        const originalWinningTeam = matchCard.dataset.winningTeam;
        if (originalWinningTeam === "1") {
          document.getElementById("team1_wins").checked = true;
        } else {
          document.getElementById("team2_wins").checked = true;
        }

        // Set the match date
        document.getElementById("date_played").value =
          matchCard.dataset.datePlayed;

        // Change Submit Button to "Edit Match"
        submitButton.textContent = "Edit Match";

        // Add "Cancel Edit" Button (if not already added)
        if (!cancelButton) {
          cancelButton = document.createElement("button");
          cancelButton.textContent = "Cancel Edit";
          cancelButton.type = "button";
          cancelButton.className = "btn btn-secondary";
          cancelButton.addEventListener("click", function () {
            window.location.reload(); // Reload page to reset form
          });

          let buttonWrapper = document.getElementById("button-wrapper");

          if (!buttonWrapper) {
            buttonWrapper = document.createElement("div");
            buttonWrapper.id = "button-wrapper";
            buttonWrapper.className = "d-flex justify-content-end gap-2 mt-3";
            submitButton.parentNode.appendChild(buttonWrapper);
          }

          buttonWrapper.innerHTML = "";
          buttonWrapper.appendChild(cancelButton);
          buttonWrapper.appendChild(submitButton);
        }

        // Form submission to use PUT
        matchForm.onsubmit = async function (e) {
          e.preventDefault();

          const csrfToken = document.querySelector(
            "[name=csrfmiddlewaretoken]"
          ).value;

          const formData = new FormData(matchForm);
          const jsonData = Object.fromEntries(formData.entries());

          console.log("Submitting edited match:", jsonData);

          try {
            let response = await fetch(`/api/games/matches/${matchId}/`, {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
              },
              body: JSON.stringify(jsonData),
            });

            if (!response.ok) {
              throw new Error(`Failed to update match ${matchId}`);
            }

            console.log("Match updated successfully.");
            window.location.reload(); // Reload page after successful edit
          } catch (error) {
            console.error("Error updating match:", error);
            alert("Failed to update the match. Please try again.");
          }
        };

        matchForm.scrollIntoView({ behavior: "smooth" });
        console.log("Form pre-filled and focused for editing:", matchId);
      }
    });
  });
});
