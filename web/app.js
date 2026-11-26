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

async function start() {
  const bootstrap = await requestJson("/api/bootstrap");
  state.priceCeiling = bootstrap.price_ceiling;
  state.cuisineChoices = bootstrap.cuisines;
  state.categoryChoices = bootstrap.categories;
  elements["price-slider"].max = String(state.priceCeiling);
  elements["price-slider"].value = String(state.priceCeiling);
  elements["price-ceiling"].textContent = bootstrap.price_ceiling_label;
  elements["dataset-count"].textContent = bootstrap.dataset_count;
  createChips(state.cuisineChoices, state.cuisines, elements["cuisine-chips"]);
  createChips(state.categoryChoices, state.categories, elements["category-chips"]);
  await renderMatches();
}

start().catch(showError);
