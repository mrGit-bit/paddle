// playerLabelUpdater.js
// Function to update form labels based on input
function updateLabel(inputElement) {
  const inputValue = inputElement.value.trim();
  const labelElement = inputElement.nextElementSibling;

  if (registeredPlayers.has(inputValue)) {
    labelElement.textContent = "Usuario Registrado✅";
  } else if (existingPlayers.has(inputValue)) {
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
