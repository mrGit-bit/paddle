console.log("passwordValidation.js loaded");
document.addEventListener("DOMContentLoaded", function () {
  const passwordField = document.getElementById("password");
  const confirmPasswordField = document.getElementById("confirm_password");

  // Add event listener only on the confirm password field
  confirmPasswordField.addEventListener("input", function () {
    if (passwordField.value !== confirmPasswordField.value) {
      confirmPasswordField.setCustomValidity("Passwords do not match.");
      confirmPasswordField.classList.add("is-invalid");
      confirmPasswordField.classList.remove("is-valid");
    } else {
      confirmPasswordField.setCustomValidity("");
      confirmPasswordField.classList.remove("is-invalid");
      confirmPasswordField.classList.add("is-valid");
    }
  });
});
