// playerLabelUpdater.js
// Purpose (match form): provide real-time feedback when typing a "new player" name.
// It warns if the typed name already exists (registered or existing) to prevent confusion.
// Server-side remains the source of truth.

(function () {
  function normName(value) {
    return (value || "").trim().toLowerCase();
  }

  function setHint(hintEl, text, kind) {
    if (!hintEl) return;
    hintEl.textContent = text || "";

    // Bootstrap-friendly hint coloring
    hintEl.classList.remove("text-success", "text-warning", "text-danger", "text-muted");
    if (!text) {
      hintEl.classList.add("text-muted");
      return;
    }
    if (kind === "registered") hintEl.classList.add("text-danger");
    else if (kind === "existing") hintEl.classList.add("text-warning");
    else if (kind === "new") hintEl.classList.add("text-success");
    else hintEl.classList.add("text-muted");
  }

  function buildLowerSet(inputSet) {
    // inputSet is expected to be a JS Set of strings (names).
    const out = new Set();
    if (!inputSet) return out;
    for (const name of inputSet) out.add(normName(name));
    return out;
  }

  document.addEventListener("DOMContentLoaded", function () {
    // These Sets are injected in match.html:
    // - registeredPlayers
    // - existingPlayers
    const registeredLower = buildLowerSet(window.registeredPlayers);
    const existingLower = buildLowerSet(window.existingPlayers);

    const newNameInputs = document.querySelectorAll("input.new-player-name");
    newNameInputs.forEach(function (input) {
      const hintId = input.id.replace("_new_name", "_new_hint");
      const hintEl = document.getElementById(hintId);

      const update = function () {
        const typed = normName(input.value);
        if (!typed) {
          setHint(hintEl, "", "empty");
          return;
        }

        if (registeredLower.has(typed)) {
          setHint(
            hintEl,
            "Este jugador ya está registrado. Se usará el perfil existente (no se creará uno nuevo).",
            "registered"
          );
          return;
        }

        if (existingLower.has(typed)) {
          setHint(
            hintEl,
            "Este jugador ya existe. Se usará el perfil existente (no se creará uno nuevo).",
            "existing"
          );
          return;
        }

        setHint(hintEl, "Nuevo jugador: se creará al guardar el partido.", "new");
      };

      input.addEventListener("input", update);
      input.addEventListener("blur", update);
      update();
    });
  });
})();
