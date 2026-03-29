document.addEventListener("DOMContentLoaded", function () {
  const table = document.querySelector("[data-ranking-sort-table]");
  if (!table) return;

  const tbody = table.querySelector("tbody");
  if (!tbody) return;

  const buttons = Array.from(table.querySelectorAll(".ranking-sort-button"));
  if (!buttons.length) return;

  let activeSort = { key: "position", direction: "asc" };

  function getRows() {
    return Array.from(tbody.querySelectorAll(".ranking-player-row"));
  }

  function parseNumber(value) {
    return Number.parseFloat(value || "0");
  }

  function rankMarkup(rank) {
    if (rank === 1) return '<strong class="rank-1">🥇</strong>';
    if (rank === 2) return '<strong class="rank-2">🥈</strong>';
    if (rank === 3) return '<strong class="rank-3">🥉</strong>';
    return String(rank);
  }

  function isCompactPositionMode() {
    return (
      (activeSort.key === "position" && activeSort.direction === "asc") ||
      (activeSort.key === "wins" && activeSort.direction === "desc")
    );
  }

  function updatePositionCells() {
    const compactMode = isCompactPositionMode();

    getRows().forEach(function (row) {
      const cell = row.querySelector("[data-position-cell]");
      if (!cell) return;

      const rank = parseNumber(row.dataset.position);
      const showCanonical = row.dataset.canonicalShowPosition === "true";

      if (compactMode) {
        cell.innerHTML = showCanonical ? rankMarkup(rank) : "&nbsp;";
        return;
      }

      cell.innerHTML = rankMarkup(rank);
    });
  }

  function updateButtons() {
    buttons.forEach(function (button) {
      const icon = button.querySelector(".ranking-sort-icon");
      const isActive = button.dataset.sortKey === activeSort.key;

      button.setAttribute("aria-pressed", isActive ? "true" : "false");

      if (!icon) return;

      icon.className = "bi ranking-sort-icon";
      if (!isActive) {
        icon.classList.add("bi-arrow-down-up");
        return;
      }

      icon.classList.add(activeSort.direction === "asc" ? "bi-caret-up-fill" : "bi-caret-down-fill");
    });
  }

  function compareRows(left, right) {
    const leftCanonical = parseNumber(left.dataset.canonicalIndex);
    const rightCanonical = parseNumber(right.dataset.canonicalIndex);

    if (activeSort.key === "position" && activeSort.direction === "asc") {
      return leftCanonical - rightCanonical;
    }

    let leftValue = 0;
    let rightValue = 0;

    if (activeSort.key === "position") {
      leftValue = parseNumber(left.dataset.position);
      rightValue = parseNumber(right.dataset.position);
    } else if (activeSort.key === "wins") {
      leftValue = parseNumber(left.dataset.wins);
      rightValue = parseNumber(right.dataset.wins);
    } else if (activeSort.key === "matches") {
      leftValue = parseNumber(left.dataset.matches);
      rightValue = parseNumber(right.dataset.matches);
    } else if (activeSort.key === "win-rate") {
      leftValue = parseNumber(left.dataset.winRate);
      rightValue = parseNumber(right.dataset.winRate);
    }

    if (leftValue !== rightValue) {
      return activeSort.direction === "asc" ? leftValue - rightValue : rightValue - leftValue;
    }

    return leftCanonical - rightCanonical;
  }

  function applySort() {
    const rows = getRows().sort(compareRows);
    rows.forEach(function (row) {
      tbody.appendChild(row);
    });
    updatePositionCells();
    updateButtons();
  }

  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      const sortKey = button.dataset.sortKey;
      const defaultDirection = button.dataset.defaultDirection || "asc";

      if (activeSort.key === sortKey) {
        activeSort.direction = activeSort.direction === "asc" ? "desc" : "asc";
      } else {
        activeSort = {
          key: sortKey,
          direction: defaultDirection,
        };
      }

      applySort();
    });
  });

  updateButtons();
  updatePositionCells();
});
