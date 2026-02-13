document.addEventListener("DOMContentLoaded", function () {
  const rows = document.querySelectorAll(".table tr[data-href]");
  rows.forEach(function (row) {
    row.style.cursor = "pointer";
    row.addEventListener("click", function (event) {
      const interactive = event.target.closest("a, button, input, select, textarea, label");
      if (interactive) return;
      const href = row.dataset.href;
      if (href) window.location.href = href;
    });
  });
});
