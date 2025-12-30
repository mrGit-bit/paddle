// path: paddle/frontend/static/frontend/js/americano_new_players_remaining.js

(function () {
  // Wait for DOM (safe even if script is loaded in <head>)
  document.addEventListener("DOMContentLoaded", function () {
    const remainingEl = document.getElementById("players-remaining");
    if (!remainingEl) return;

    const numPlayersEl = document.querySelector('input[name="num_players"]');
    const registeredEl = document.querySelector('select[name="players"]');
    const newPlayersEl = document.querySelector('textarea[name="new_players"]');

    if (!numPlayersEl || !registeredEl || !newPlayersEl) {
      remainingEl.textContent = "Jugadores restantes: —";
      return;
    }

    function countRegisteredSelected() {
      return Array.from(registeredEl.selectedOptions || []).length;
    }

    // One player per line
    function countNewPlayers() {
      return (newPlayersEl.value || "")
        .split("\n")
        .map((s) => s.trim())
        .filter((s) => s.length > 0).length;
    }

    function updateRemaining() {
      const target = parseInt(numPlayersEl.value, 10);
      const selected = countRegisteredSelected() + countNewPlayers();

      if (Number.isNaN(target) || target <= 0) {
        remainingEl.textContent = "Jugadores restantes: —";
        remainingEl.className = "small text-muted";
        return;
      }

      const remaining = target - selected;

      if (remaining > 0) {
        remainingEl.textContent = `Jugadores restantes: ${remaining}`;
        remainingEl.className = "small text-muted";
      } else if (remaining === 0) {
        remainingEl.textContent = "Jugadores restantes: 0 (completo!!)";
        remainingEl.className = "small text-success fw-bold";
      } else {
        remainingEl.textContent = `Has seleccionado ${Math.abs(remaining)} jugador(es) de más.`;
        remainingEl.className = "small text-danger";
      }
    }

    numPlayersEl.addEventListener("input", updateRemaining);
    registeredEl.addEventListener("change", updateRemaining);
    newPlayersEl.addEventListener("input", updateRemaining);

    updateRemaining();
  });
})();
