document.addEventListener("DOMContentLoaded", function () {
  // Select the radio buttons and team cards
  const team1WinsRadio = document.getElementById("team1_wins");
  const team2WinsRadio = document.getElementById("team2_wins");

  const team1Card = document.querySelector(".col-sm-6.mb-3 .card");
  const team2Card = document.querySelector(".col-sm-6:last-child .card");

  // Function to update background class
  function updateBackground() {
    // Remove previous background class
    team1Card.classList.remove("text-bg-success");
    team2Card.classList.remove("text-bg-success");

    // Apply new background based on selection
    if (team1WinsRadio.checked) {
      team1Card.classList.add("text-bg-success");
    } else if (team2WinsRadio.checked) {
      team2Card.classList.add("text-bg-success");
    }
  }

  // Attach event listeners to radio buttons
  team1WinsRadio.addEventListener("change", updateBackground);
  team2WinsRadio.addEventListener("change", updateBackground);
});
