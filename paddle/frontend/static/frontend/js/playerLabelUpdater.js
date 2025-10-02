// playerLabelUpdater.js
// Function to update form labels based on input (case-insensitive comparison)
function updateLabel(inputElement) {
  const inputValue = inputElement.value.trim().toLowerCase();
  const labelElement = inputElement.nextElementSibling;

  // Convert all player names to lower case for comparison
  const registeredPlayersLower = new Set(Array.from(registeredPlayers, name => name.toLowerCase()));
  const existingPlayersLower = new Set(Array.from(existingPlayers, name => name.toLowerCase()));


  if (registeredPlayersLower.has(inputValue)) {
    labelElement.textContent = "Usuario Registrado✅";
  } else if (existingPlayersLower.has(inputValue)) {
    labelElement.textContent = "Jugador Existente✔️";
  } else {
    labelElement.textContent = "Nuevo Jugador en el ranking❓";
  }
}

// Attach event listeners to relevant input fields
document.addEventListener("DOMContentLoaded", () => {
  const playerInputs = document.querySelectorAll("#team1_player2, #team2_player1, #team2_player2");
  playerInputs.forEach(input => {
    input.addEventListener("input", (event) => updateLabel(event.target));
  });
});
