// playerLabelUpdater.js
// Function to update form labels based on input
function updateLabel(inputElement) {
  const inputValue = inputElement.value.trim();
  const labelElement = inputElement.nextElementSibling;

  if (registeredPlayers.has(inputValue)) {
    labelElement.textContent = "Registered User";
  } else if (existingPlayers.has(inputValue)) {
    labelElement.textContent = "Existing Player";
  } else {
    labelElement.textContent = "New Player";
  }
}

// Attach event listeners to relevant input fields
document.addEventListener("DOMContentLoaded", () => {
  const playerInputs = document.querySelectorAll("#team1_player2, #team2_player1, #team2_player2");
  playerInputs.forEach(input => {
    input.addEventListener("input", (event) => updateLabel(event.target));
  });
});
