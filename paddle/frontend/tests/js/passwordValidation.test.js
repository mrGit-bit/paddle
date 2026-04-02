const test = require("node:test");
const assert = require("node:assert/strict");

const { initPasswordValidation } = require("../../static/frontend/js/passwordValidation.js");

function createClassList() {
  const values = new Set();
  return {
    add(name) {
      values.add(name);
    },
    remove(name) {
      values.delete(name);
    },
    contains(name) {
      return values.has(name);
    },
  };
}

function createInput({ value = "", valid = true } = {}) {
  return {
    value,
    valid,
    listeners: {},
    classList: createClassList(),
    customValidity: "",
    addEventListener(event, handler) {
      this.listeners[event] = handler;
    },
    checkValidity() {
      return this.valid;
    },
    setCustomValidity(message) {
      this.customValidity = message;
    },
  };
}

function createDocument() {
  const button = { disabled: false };
  const form = {
    querySelectorAll(selector) {
      return selector === 'button[type="submit"]' ? [button] : [];
    },
  };
  const email = createInput({ valid: true });
  const confirmEmail = createInput({ valid: true });
  const password = createInput({ valid: true });
  const confirmPassword = createInput({ valid: true });

  const elements = {
    "user-form": form,
    email,
    confirm_email: confirmEmail,
    password,
    confirm_password: confirmPassword,
  };

  return {
    elements,
    button,
    getElementById(id) {
      return elements[id] || null;
    },
  };
}

test("initPasswordValidation clears invalid state and re-enables submit for matching pairs", () => {
  const document = createDocument();
  const { email, confirm_email: confirmEmail, password, confirm_password: confirmPassword } =
    document.elements;

  initPasswordValidation(document);
  assert.equal(document.button.disabled, true);

  email.value = "test@example.com";
  email.listeners.input();
  confirmEmail.value = "test@example.com";
  confirmEmail.listeners.input();
  password.value = "pass12345";
  password.listeners.input();
  confirmPassword.value = "pass12345";
  confirmPassword.listeners.input();

  assert.equal(confirmEmail.classList.contains("is-invalid"), false);
  assert.equal(confirmEmail.classList.contains("is-valid"), true);
  assert.equal(confirmPassword.classList.contains("is-invalid"), false);
  assert.equal(confirmPassword.classList.contains("is-valid"), true);
  assert.equal(document.button.disabled, false);
});
