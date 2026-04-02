function initPasswordValidation(doc) {
  const currentDocument = doc || (typeof document !== "undefined" ? document : null);
  if (!currentDocument) {
    return;
  }

  const form = currentDocument.getElementById("user-form");
  if (!form) {
    return;
  }

  const submitButtons = Array.from(form.querySelectorAll('button[type="submit"]'));
  const normalize = (value, mode) => {
    if (mode === "email") {
      return value.trim().toLowerCase();
    }
    return value;
  };

  const pairs = [
    {
      target: currentDocument.getElementById("email"),
      confirm: currentDocument.getElementById("confirm_email"),
      mode: "email",
      mismatchMessage: "Los correos electrónicos no coinciden.",
      touched: false,
    },
    {
      target: currentDocument.getElementById("password"),
      confirm: currentDocument.getElementById("confirm_password"),
      mode: "raw",
      mismatchMessage: "Las contraseñas no coinciden.",
      touched: false,
    },
  ].filter((pair) => pair.target && pair.confirm);

  if (!pairs.length) {
    return;
  }

  const evaluatePair = (pair) => {
    const targetValue = normalize(pair.target.value, pair.mode);
    const confirmValue = normalize(pair.confirm.value, pair.mode);
    const hasInput = pair.target.value.length > 0 || pair.confirm.value.length > 0;
    const isMatch = targetValue.length > 0 && targetValue === confirmValue;
    // Clear pair-specific mismatch state before checking native field validity.
    pair.confirm.setCustomValidity("");

    const targetFormatValid = pair.target.checkValidity();
    const confirmFormatValid = pair.confirm.checkValidity();

    if (!hasInput) {
      pair.confirm.setCustomValidity("Este campo es obligatorio.");
      pair.confirm.classList.remove("is-valid");
      pair.confirm.classList.remove("is-invalid");
      return false;
    }

    if (!pair.touched) {
      pair.confirm.setCustomValidity(pair.mismatchMessage);
      pair.confirm.classList.remove("is-valid");
      pair.confirm.classList.remove("is-invalid");
      return false;
    }

    if (!targetFormatValid || !confirmFormatValid) {
      pair.confirm.classList.add("is-invalid");
      pair.confirm.classList.remove("is-valid");
      return false;
    }

    if (!isMatch) {
      pair.confirm.setCustomValidity(pair.mismatchMessage);
      pair.confirm.classList.add("is-invalid");
      pair.confirm.classList.remove("is-valid");
      return false;
    }

    pair.confirm.setCustomValidity("");
    pair.confirm.classList.remove("is-invalid");
    pair.confirm.classList.add("is-valid");
    return true;
  };

  const syncSubmitState = () => {
    const allPairsValid = pairs.every((pair) => evaluatePair(pair));
    submitButtons.forEach((button) => {
      button.disabled = !allPairsValid;
    });
  };

  pairs.forEach((pair) => {
    pair.touched = pair.confirm.value.length > 0;
    pair.target.addEventListener("input", syncSubmitState);
    pair.confirm.addEventListener("input", () => {
      pair.touched = true;
      syncSubmitState();
    });
  });

  syncSubmitState();
}

if (typeof document !== "undefined") {
  document.addEventListener("DOMContentLoaded", function () {
    initPasswordValidation(document);
  });
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { initPasswordValidation };
}
