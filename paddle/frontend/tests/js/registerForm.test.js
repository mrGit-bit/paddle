const test = require("node:test");
const assert = require("node:assert/strict");

const { initRegisterForm } = require("../../static/frontend/js/registerForm.js");

function createClassList(initial = []) {
  const values = new Set(initial);
  return {
    add(name) {
      values.add(name);
    },
    remove(name) {
      values.delete(name);
    },
    toggle(name, force) {
      if (force) {
        values.add(name);
      } else {
        values.delete(name);
      }
    },
    contains(name) {
      return values.has(name);
    },
  };
}

function createOption(value, textContent, groupId = undefined) {
  return {
    value,
    textContent,
    dataset: groupId === undefined ? {} : { groupId },
    selected: false,
  };
}

function createSelect(options, value = "") {
  const select = {
    _options: options,
    _value: value,
    listeners: {},
    addEventListener(event, handler) {
      this.listeners[event] = handler;
    },
    querySelectorAll(selector) {
      return selector === "option" ? this._options : [];
    },
    appendChild(option) {
      this._options.push(option);
    },
    get options() {
      return this._options;
    },
    get value() {
      return this._value;
    },
    set value(nextValue) {
      this._value = nextValue;
      this._options.forEach((option) => {
        option.selected = option.value === nextValue;
      });
    },
  };

  Object.defineProperty(select, "innerHTML", {
    get() {
      return "";
    },
    set() {
      select._options = [];
      select._value = "";
    },
  });

  select.value = value;
  return select;
}

function createDocument() {
  const groupChoice = {
    value: "",
    listeners: {},
    addEventListener(event, handler) {
      this.listeners[event] = handler;
    },
  };
  const newGroupWrapper = { classList: createClassList(["d-none"]) };
  const newGroupInput = {
    required: false,
    setAttribute(name) {
      if (name === "required") {
        this.required = true;
      }
    },
    removeAttribute(name) {
      if (name === "required") {
        this.required = false;
      }
    },
  };
  const playerWrapper = { classList: createClassList(["d-none"]) };
  const playerSelect = createSelect(
    [
      createOption("", "No, soy un nuevo jugador"),
      createOption("1", "Ana", "10"),
      createOption("2", "Luis", "20"),
    ],
    ""
  );

  const elements = {
    group_choice: groupChoice,
    "new-group-name-wrapper": newGroupWrapper,
    new_group_name: newGroupInput,
    "player-id-wrapper": playerWrapper,
    player_id: playerSelect,
  };

  return {
    elements,
    getElementById(id) {
      return elements[id] || null;
    },
    createElement() {
      return createOption("", "");
    },
  };
}

test("initRegisterForm toggles create-group and existing-player fields", () => {
  const document = createDocument();
  initRegisterForm(document);

  const groupChoice = document.elements.group_choice;
  const newGroupWrapper = document.elements["new-group-name-wrapper"];
  const newGroupInput = document.elements.new_group_name;
  const playerWrapper = document.elements["player-id-wrapper"];
  const playerSelect = document.elements.player_id;

  assert.equal(newGroupWrapper.classList.contains("d-none"), true);
  assert.equal(playerWrapper.classList.contains("d-none"), true);
  assert.deepEqual(
    playerSelect.options.map((option) => option.textContent),
    ["No, soy un nuevo jugador"]
  );

  groupChoice.value = "10";
  groupChoice.listeners.change();

  assert.equal(newGroupWrapper.classList.contains("d-none"), true);
  assert.equal(playerWrapper.classList.contains("d-none"), false);
  assert.deepEqual(
    playerSelect.options.map((option) => option.textContent),
    ["No, soy un nuevo jugador", "Ana"]
  );

  groupChoice.value = "__create__";
  groupChoice.listeners.change();

  assert.equal(newGroupWrapper.classList.contains("d-none"), false);
  assert.equal(playerWrapper.classList.contains("d-none"), true);
  assert.equal(newGroupInput.required, true);
});
