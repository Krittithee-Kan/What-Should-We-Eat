const wheelColors = ["#ffffff", "#fbcfe8", "#e6f4ff", "#e8f6eb", "#fff9e8", "#fff0e4"];

const state = {
  cuisines: new Set(),
  categories: new Set(),
  cuisineChoices: [],
  categoryChoices: [],
  priceCeiling: 1000,
  spinning: false,
  rotation: 0,
  matchRequest: 0,
};

const elements = Object.fromEntries([
  "dataset-count", "price-slider", "price-output", "price-ceiling", "cuisine-chips",
  "category-chips", "spin-matches", "surprise", "reset", "match-count",
  "restaurant-list", "result-eyebrow", "result-title", "result-detail", "wheel", "wheel-count",
].map((id) => [id, document.getElementById(id)]));

async function requestJson(path, payload) {
  const options = payload === undefined
    ? {}
    : {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      };
  const response = await fetch(path, options);
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || `Request failed (${response.status})`);
  return body;
}

function currentFilters() {
  return {
    max_price: Number(elements["price-slider"].value),
    cuisines: [...state.cuisines],
    categories: [...state.categories],
  };
}

function createChips(choices, selected, container) {
  container.replaceChildren();
  choices.forEach(({ value, label }) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "chip";
    button.textContent = label;
    button.setAttribute("aria-pressed", String(selected.has(value)));
    button.addEventListener("click", () => {
      selected.has(value) ? selected.delete(value) : selected.add(value);
      button.setAttribute("aria-pressed", String(selected.has(value)));
      renderMatches();
    });
    container.append(button);
  });
}

function setWheel(count) {
  const segmentCount = Math.min(count, 24);
  elements["wheel-count"].textContent = String(count);
  if (!segmentCount) {
    elements.wheel.style.background = "#f2df9a";
    return;
  }
  const step = 360 / segmentCount;
  const stops = Array.from({ length: segmentCount }, (_, index) => {
    const color = wheelColors[index % wheelColors.length];
    return `${color} ${index * step}deg ${(index + 1) * step}deg`;
  });
  elements.wheel.style.background = `conic-gradient(${stops.join(",")})`;
}

function renderRestaurantList(result) {
  elements["match-count"].textContent = result.match_count;
  elements["price-output"].textContent = result.price_label;
  elements["restaurant-list"].replaceChildren();

  if (!result.matches.length) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    const heading = document.createElement("h3");
    heading.textContent = "No restaurant matches every filter yet";
    const copy = document.createElement("p");
    copy.textContent = "Try a higher budget or remove one of your selections.";
    empty.append(heading, copy);
    elements["restaurant-list"].append(empty);
    setWheel(0);
    return;
  }

  result.matches.forEach((match, index) => {
    const card = document.createElement("article");
    card.className = "restaurant-card";
    const number = document.createElement("div");
    number.className = "restaurant-number";
    number.textContent = String(index + 1).padStart(2, "0");
    const copy = document.createElement("div");
    const name = document.createElement("h3");
    name.className = "restaurant-name";
    name.textContent = match.name;
    const meta = document.createElement("p");
    meta.className = "restaurant-meta";
    meta.textContent = match.meta;
    copy.append(name, meta);
    card.append(number, copy);
    elements["restaurant-list"].append(card);
  });

  setWheel(result.dish_count);
}

async function renderMatches() {
  const requestNumber = ++state.matchRequest;
  try {
    const result = await requestJson("/api/matches", currentFilters());
    if (requestNumber === state.matchRequest) renderRestaurantList(result);
  } catch (error) {
    if (requestNumber === state.matchRequest) showError(error);
  }
}

function setSpinning(spinning) {
  state.spinning = spinning;
  elements["spin-matches"].disabled = spinning;
  elements.surprise.disabled = spinning;
}

function showError(error) {
  elements["result-eyebrow"].textContent = "SOMETHING WENT WRONG";
  elements["result-title"].textContent = "The Python service could not complete the request";
  elements["result-detail"].textContent = error.message;
  setSpinning(false);
}

function showNoMatch() {
  elements["result-eyebrow"].textContent = "NO MENU YET";
  elements["result-title"].textContent = "No dish matches every filter";
  elements["result-detail"].textContent = "Reset one or more filters, then try again.";
  setSpinning(false);
}

function spinToSelection(result) {
  const { selected, candidate_count: candidateCount } = result;
  setWheel(candidateCount);
  elements["result-eyebrow"].textContent = "SPINNING THE WHEEL";
  elements["result-title"].textContent = "Finding your dish…";
  elements["result-detail"].textContent = result.helper_text;

  const segmentCount = Math.min(candidateCount, 24);
  const visualIndex = selected.index % segmentCount;
  const segmentAngle = 360 / segmentCount;
  const targetCenter = (visualIndex + 0.5) * segmentAngle;
  const delta = ((360 - targetCenter - (state.rotation % 360)) % 360) + 1440;
  state.rotation += delta;
  elements.wheel.style.transition = "transform 1.8s cubic-bezier(.16,.78,.18,1)";
  requestAnimationFrame(() => {
    elements.wheel.style.transform = `rotate(${state.rotation}deg)`;
  });
  window.setTimeout(() => {
    elements["result-eyebrow"].textContent = "YOUR MENU";
    elements["result-title"].textContent = selected.dish_name;
    elements["result-detail"].textContent = selected.detail;
    setSpinning(false);
  }, 1820);
}

async function requestSelection(path, payload) {
  if (state.spinning) return;
  setSpinning(true);
  try {
    const result = await requestJson(path, payload);
    if (!result.selected) {
      showNoMatch();
      return;
    }
    spinToSelection(result);
  } catch (error) {
    showError(error);
  }
}

function resetFilters() {
  state.cuisines.clear();
  state.categories.clear();
  elements["price-slider"].value = String(state.priceCeiling);
  elements["price-output"].textContent = "Any price";
  createChips(state.cuisineChoices, state.cuisines, elements["cuisine-chips"]);
  createChips(state.categoryChoices, state.categories, elements["category-chips"]);
  elements["result-eyebrow"].textContent = "Ready when you are";
  elements["result-title"].textContent = "Set your filters, then spin for a dish";
  elements["result-detail"].textContent = "Ready to pick your next meal";
  renderMatches();
}

elements["price-slider"].addEventListener("input", renderMatches);
elements["spin-matches"].addEventListener("click", () => {
  requestSelection("/api/spin", currentFilters());
});
elements.surprise.addEventListener("click", () => {
  requestSelection("/api/surprise", {});
});
elements.reset.addEventListener("click", resetFilters);

const manage = Object.fromEntries([
  "manage-open", "manage-dialog", "manage-close", "manage-notice", "add-form",
  "add-name", "dish-rows", "add-dish", "form-errors", "manage-list",
].map((id) => [id, document.getElementById(id)]));

function showStorageNotice(message) {
  elements["result-eyebrow"].textContent = "SAVED LIST";
  elements["result-title"].textContent = "Some saved data could not be loaded";
  elements["result-detail"].textContent = message;
}

function setNotice(message) {
  manage["manage-notice"].textContent = message;
  manage["manage-notice"].hidden = !message;
}

function createSelect(choices, className) {
  const select = document.createElement("select");
  select.className = className;
  choices.forEach(({ value, label }) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    select.append(option);
  });
  return select;
}

function labelled(text, control) {
  const label = document.createElement("label");
  label.className = "field";
  const caption = document.createElement("span");
  caption.textContent = text;
  label.append(caption, control);
  return label;
}

function updateRemoveButtons() {
  const rows = manage["dish-rows"].querySelectorAll(".dish-row");
  rows.forEach((row) => {
    row.querySelector(".remove-dish").disabled = rows.length === 1;
  });
}

function addDishRow() {
  const row = document.createElement("div");
  row.className = "dish-row";

  const name = document.createElement("input");
  name.type = "text";
  name.className = "dish-name";
  name.placeholder = "Optional";

  const price = document.createElement("input");
  price.type = "number";
  price.min = "0";
  price.step = "1";
  price.className = "dish-price";

  const remove = document.createElement("button");
  remove.type = "button";
  remove.className = "button button-secondary remove-dish";
  remove.textContent = "Remove";
  remove.addEventListener("click", () => {
    row.remove();
    updateRemoveButtons();
  });

  row.append(
    labelled("Dish name", name),
    labelled("Cuisine", createSelect(state.cuisineChoices, "dish-cuisine")),
    labelled("Dish type", createSelect(state.categoryChoices, "dish-category")),
    labelled("Price (฿)", price),
    remove,
  );
  manage["dish-rows"].append(row);
  updateRemoveButtons();
}

function resetAddForm() {
  manage["add-name"].value = "";
  manage["dish-rows"].replaceChildren();
  addDishRow();
  showFormErrors([]);
}

function readAddForm() {
  return {
    name: manage["add-name"].value,
    menu: [...manage["dish-rows"].querySelectorAll(".dish-row")].map((row) => ({
      dish: row.querySelector(".dish-name").value,
      cuisine: row.querySelector(".dish-cuisine").value,
      category: row.querySelector(".dish-category").value,
      price: row.querySelector(".dish-price").value,
    })),
  };
}

function showFormErrors(errors) {
  manage["form-errors"].replaceChildren();
  errors.forEach((error) => {
    const item = document.createElement("li");
    item.textContent = error;
    manage["form-errors"].append(item);
  });
  manage["form-errors"].hidden = errors.length === 0;
}

async function refreshDataset() {
  const bootstrap = await requestJson("/api/bootstrap");
  const slider = elements["price-slider"];
  const wasAnyPrice = Number(slider.value) >= Number(slider.max);
  state.priceCeiling = bootstrap.price_ceiling;
  slider.max = String(state.priceCeiling);
  if (wasAnyPrice) slider.value = String(state.priceCeiling);
  elements["price-ceiling"].textContent = bootstrap.price_ceiling_label;
  elements["dataset-count"].textContent = bootstrap.dataset_count;
  await renderMatches();
}

async function renderManageList() {
  const { restaurants } = await requestJson("/api/restaurants");
  manage["manage-list"].replaceChildren();
  restaurants.forEach((restaurant) => {
    const item = document.createElement("li");
    const copy = document.createElement("div");
    const name = document.createElement("strong");
    name.textContent = restaurant.name;
    const meta = document.createElement("span");
    meta.textContent = `${restaurant.dish_count} ${restaurant.dish_count === 1 ? "dish" : "dishes"}`;
    copy.append(name, meta);

    const remove = document.createElement("button");
    remove.type = "button";
    remove.className = "button button-secondary delete-restaurant";
    remove.textContent = "Delete";
    remove.addEventListener("click", () => deleteRestaurant(restaurant, remove));

    item.append(copy, remove);
    manage["manage-list"].append(item);
  });
}

async function deleteRestaurant(restaurant, button) {
  if (button.dataset.confirm !== "yes") {
    button.dataset.confirm = "yes";
    button.textContent = "Click again to delete";
    button.classList.add("confirming");
    return;
  }
  button.disabled = true;
  try {
    await requestJson("/api/restaurants/delete", { id: restaurant.id });
    setNotice(`Deleted “${restaurant.name}”.`);
    await renderManageList();
    await refreshDataset();
  } catch (error) {
    setNotice(error.message);
    button.disabled = false;
  }
}

async function submitAddForm(event) {
  event.preventDefault();
  const response = await fetch("/api/restaurants/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(readAddForm()),
  });
  const body = await response.json();
  if (!response.ok) {
    showFormErrors(body.errors || [body.error || "The restaurant could not be saved."]);
    return;
  }
  setNotice(`Saved “${body.name}”.`);
  resetAddForm();
  await renderManageList();
  await refreshDataset();
}

async function openManage() {
  setNotice("");
  resetAddForm();
  manage["manage-dialog"].showModal();
  try {
    await renderManageList();
  } catch (error) {
    setNotice(error.message);
  }
}

manage["manage-open"].addEventListener("click", openManage);
manage["manage-close"].addEventListener("click", () => manage["manage-dialog"].close());
manage["add-dish"].addEventListener("click", addDishRow);
manage["add-form"].addEventListener("submit", (event) => {
  submitAddForm(event).catch((error) => showFormErrors([error.message]));
});

async function start() {
  const bootstrap = await requestJson("/api/bootstrap");
  state.priceCeiling = bootstrap.price_ceiling;
  state.cuisineChoices = bootstrap.cuisines;
  state.categoryChoices = bootstrap.categories;
  elements["price-slider"].max = String(state.priceCeiling);
  elements["price-slider"].value = String(state.priceCeiling);
  elements["price-ceiling"].textContent = bootstrap.price_ceiling_label;
  elements["dataset-count"].textContent = bootstrap.dataset_count;
  if (bootstrap.storage_message) showStorageNotice(bootstrap.storage_message);
  createChips(state.cuisineChoices, state.cuisines, elements["cuisine-chips"]);
  createChips(state.categoryChoices, state.categories, elements["category-chips"]);
  await renderMatches();
}

start().catch(showError);
