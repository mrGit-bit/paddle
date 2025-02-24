console.log("editUserProfile.js loaded");

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOMContentLoaded event fired.");

  const form = document.getElementById("user-form");
  const saveBtn = document.getElementById("save-btn");
  const cancelBtn = document.getElementById("cancel-btn");

  const emailField = form.querySelector("input[name='email']");
  let originalEmail = emailField.value;

  // Store initial email values
  function storeInitialEmail() {
    console.log(`Storing original email:"${originalEmail}"`);    
  }

  // Reset email field to its original value
  function resetForm() {
    console.log("Resetting form...");
    emailField.value = originalEmail;        
    saveBtn.setAttribute("disabled", "true");
    cancelBtn.setAttribute("disabled", "true");
    console.log("Form reset to original state.");
  }

  // Enable buttons when email field is edited
  emailField.addEventListener("input", function () {    
    if (emailField.value !== originalEmail) {
      saveBtn.removeAttribute("disabled");
      cancelBtn.removeAttribute("disabled");
      console.log(`Email field changed to "${emailField.value}"`);
    }     
  });

  // Handle cancel button click
  cancelBtn.addEventListener("click", function () {
    console.log("Cancel button clicked.");
    resetForm();
  });

  // Handle form submission (only send email field if modified)
  form.addEventListener("submit", function (e) {
    e.preventDefault();

    if (emailField.value === originalEmail) {
      console.log("No changes to submit.");
      return;
    }

    // Prepare payload with only modified fields
    const payload = {
      email: emailField.value,
    };

    console.log("Submitting modified email:", payload);

    // PATCH request for updating email
    fetch(form.action, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
      },
      body: JSON.stringify(payload),
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        // Display the error dynamically
        const errorContainer = document.getElementById('error-container');
        errorContainer.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
      } else {
        console.log("Update successful.");
      }
    })
      .catch(err => console.error("Error submitting form:", err));
  });

  // Initialize the form
  console.log("Initializing form...");
  storeInitialEmail();
  console.log("Form initialized.");
});
