document.addEventListener("DOMContentLoaded", function () {
  const toggleButtons = Array.from(document.querySelectorAll("[data-password-toggle]"));

  toggleButtons.forEach((button) => {
    const targetId = button.dataset.passwordTarget;
    const input = targetId ? document.getElementById(targetId) : null;
    const icon = button.querySelector("i");
    const label = button.querySelector(".visually-hidden");

    if (!input || !icon || !label) {
      return;
    }

    const syncButtonState = (isVisible) => {
      icon.classList.toggle("bi-eye", !isVisible);
      icon.classList.toggle("bi-eye-slash", isVisible);
      label.textContent = isVisible ? "Ocultar contraseña" : "Mostrar contraseña";
      button.setAttribute("aria-label", label.textContent);
      button.setAttribute("aria-pressed", isVisible ? "true" : "false");
    };

    syncButtonState(false);

    button.addEventListener("click", () => {
      const shouldShow = input.type === "password";

      input.type = shouldShow ? "text" : "password";
      syncButtonState(shouldShow);
      input.focus({ preventScroll: true });
    });
  });
});
