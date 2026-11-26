# What Should We Eat?

## Team and purpose
- Members:
  - Krittithee Kanjanapinchote — 6580988 — Krittithee-Kan
  - Siriphanaphon Sirikun — 6680085 — Blimmy
  - Napat Oonsamatham — 6680964 — napat-oon
- Intended users and problem: [who needs this and why, in your own words]

## Core workflow and scope
- Feature 1 — Manage a saved restaurant list: add, edit and delete restaurants and their menus (each dish has a cuisine, a category and a price). The list is kept after closing and reopening the app.
- Feature 2 — Filter and pick: choose conditions (price, cuisine and category ) and get one restaurant picked only from the restaurants that match all of them.
- Important behaviour rules:
  - Each restaurant has a menu of at least one dish. Price, cuisine and category belong to each dish, not to the restaurant.
  - Price = the price of that dish for one person, in whole baht.
  - "Up to 60 baht" means 60 or less; a 60-baht dish does match.
  - Cuisine and category are chosen from fixed lists in `app/constants.py`. Each dish has exactly one cuisine and one category.
  - A restaurant matches only if at least one single dish passes all chosen filters by itself.
  - If nothing matches, the app says so and does not pick anything. It never drops a filter to force a result.
  - The user can choose any filters they want: one, several, or none. Filters that are not chosen are ignored.
  - When adding a restaurant: a restaurant name and at least one dish are required; each dish needs a cuisine, a category and a price above or equal to 0. A dish name is optional. Invalid input is rejected and the saved list does not change.
  - A damaged save file does not crash the app; broken entries are skipped and the user is told how many.
- Simulations and exclusions: one computer, one saved list, no accounts, no maps or distance (we don't know where the user is), no online voting, no runtime AI. Restaurant data is typed in by hand.

## Setup, run and test
- Runtime versions and dependencies: Python; libraries are listed in
  `requirements.txt`. The web server uses only the Python standard library.
- Install: `pip install -r requirements.txt`
- Run web app: `python -m app.web`, then open `http://localhost:5173`
- Run desktop app: `python -m app.main`
- Test: `pytest`
- Sample data: `app/sample/restaurants.py` includes 19 restaurants and 266
  dishes with English display names; the desktop app loads it automatically.

## Reused work and limitations
- Libraries, starter templates, code and assets: pytest (testing); tkinter
  (desktop UI); Python's built-in HTTP server (web UI).
- Known limitations: [what users should know]
