document.addEventListener("DOMContentLoaded", function () {
  const strips = document.querySelectorAll(".medallero-icon-strip");
  if (!strips.length) {
    return;
  }

  function updateStrip(strip) {
    const icons = Array.from(strip.querySelectorAll(".medallero-medal-icon-small"));
    if (icons.length <= 1) {
      strip.style.setProperty("--medallero-icon-overlap", "0px");
      return;
    }

    strip.style.setProperty("--medallero-icon-overlap", "0px");

    const styles = window.getComputedStyle(strip);
    const gap = parseFloat(styles.columnGap || styles.gap) || 0;
    const iconWidth = icons[0].getBoundingClientRect().width;
    const fullWidth = (icons.length * iconWidth) + ((icons.length - 1) * gap);
    const availableWidth = strip.getBoundingClientRect().width;
    const excessWidth = Math.max(0, fullWidth - availableWidth);
    const requiredOverlap = excessWidth / (icons.length - 1);
    const maxOverlap = Math.max(0, iconWidth - 4);

    strip.style.setProperty(
      "--medallero-icon-overlap",
      `${Math.min(requiredOverlap, maxOverlap).toFixed(2)}px`,
    );
  }

  function updateAllStrips() {
    strips.forEach(updateStrip);
  }

  updateAllStrips();

  if ("ResizeObserver" in window) {
    const observer = new ResizeObserver(updateAllStrips);
    strips.forEach((strip) => observer.observe(strip));
    return;
  }

  window.addEventListener("resize", updateAllStrips);
});
