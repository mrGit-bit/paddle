function initRegisterForm(doc) {
  const currentDocument = doc || (typeof document !== "undefined" ? document : null);
  if (!currentDocument) {
    return;
  }

  const groupChoice = currentDocument.getElementById("group_choice");
  const newGroupWrapper = currentDocument.getElementById("new-group-name-wrapper");
  const newGroupInput = currentDocument.getElementById("new_group_name");
  const playerWrapper = currentDocument.getElementById("player-id-wrapper");
  const playerSelect = currentDocument.getElementById("player_id");
  const createValue = "__create__";

  if (!groupChoice || !newGroupWrapper || !newGroupInput || !playerWrapper || !playerSelect) {
    return;
  }

  const allPlayerOptions = Array.from(playerSelect.querySelectorAll("option"))
    .slice(1)
    .map(function (option) {
      return {
        value: option.value,
        label: option.textContent,
        groupId: option.dataset.groupId,
      };
    });

  function rebuildPlayerOptions(groupId) {
    const selectedValue = playerSelect.value;
    playerSelect.innerHTML = "";

    const placeholder = currentDocument.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "No, soy un nuevo jugador";
    playerSelect.appendChild(placeholder);

    allPlayerOptions
      .filter(function (option) {
        return option.groupId === groupId;
      })
      .forEach(function (option) {
        const node = currentDocument.createElement("option");
        node.value = option.value;
        node.textContent = option.label;
        node.dataset.groupId = option.groupId;
        if (selectedValue === option.value) {
          node.selected = true;
        }
        playerSelect.appendChild(node);
      });

    if (!Array.from(playerSelect.options).some(function (option) {
      return option.selected;
    })) {
      playerSelect.value = "";
    }
  }

  function syncGroupFields() {
    const selectedGroup = groupChoice.value;
    const isCreate = selectedGroup === createValue;

    newGroupWrapper.classList.toggle("d-none", !isCreate);
    playerWrapper.classList.toggle("d-none", isCreate || !selectedGroup);

    if (isCreate) {
      newGroupInput.setAttribute("required", "required");
      playerSelect.value = "";
    } else {
      newGroupInput.removeAttribute("required");
    }

    if (!isCreate && selectedGroup) {
      rebuildPlayerOptions(selectedGroup);
    } else if (!selectedGroup) {
      rebuildPlayerOptions("__none__");
    }
  }

  groupChoice.addEventListener("change", syncGroupFields);
  syncGroupFields();
}

if (typeof document !== "undefined") {
  document.addEventListener("DOMContentLoaded", function () {
    initRegisterForm(document);
  });
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { initRegisterForm };
}
