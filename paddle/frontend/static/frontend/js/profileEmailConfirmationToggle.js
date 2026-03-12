document.addEventListener("DOMContentLoaded", function () {
  const emailField = document.getElementById("email");
  const confirmContainer = document.getElementById("profile-confirm-email-container");
  const confirmField = document.getElementById("confirm_email");

  if (!emailField || !confirmContainer || !confirmField) {
    return;
  }

  const normalizeEmail = (value) => value.trim().toLowerCase();
  const originalEmail = normalizeEmail(emailField.dataset.originalEmail || "");

  const syncVisibility = () => {
    const currentEmail = normalizeEmail(emailField.value);
    const shouldShow = currentEmail !== originalEmail;

    confirmContainer.classList.toggle("d-none", !shouldShow);

    if (!shouldShow) {
      confirmField.value = "";
      confirmField.classList.remove("is-invalid");
      confirmField.classList.remove("is-valid");
    }
  };

  emailField.addEventListener("input", syncVisibility);
  syncVisibility();
});
