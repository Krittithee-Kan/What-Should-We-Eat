# What Should We Eat?

## Team and purpose
- Members:
  - Krittithee Kanjanapinchote — [student ID] — [GitHub username]
  - Siriphanaphon Sirikun — [student ID] — [GitHub username]
  - Napat Oonsamatham — [student ID] — [GitHub username]
- Intended users and problem: [who needs this and why, in your own words]

## Core workflow and scope
- Feature 1 — Manage a saved restaurant list: add, edit and delete restaurants. The list is kept after closing and reopening the app.
- Feature 2 — Filter and pick: choose conditions (price and food type) and get one restaurant picked only from the restaurants that match all of them.
- Important behaviour rules:
  - Price = usual price of one main dish for one person, in whole baht.
  - "Under 60 baht" means strictly less than 60 (a 60-baht restaurant does not match).
  - Food type is chosen from a fixed list.
  - When several filters are chosen, a restaurant must match all of them.
  - If nothing matches, the app says so and does not pick anything. It never drops a filter to force a result.
  - Invalid input (empty name, price 0 or less, letters in price) is rejected and the saved list does not change.
  - A damaged save file does not crash the app; broken entries are skipped and the user is told how many.
- Simulations and exclusions: one computer, one saved list, no accounts, no maps or distance (we don't know where the user is), no online voting, no runtime AI. Restaurant data is typed in by hand.

## Setup, run and test
- Runtime versions and dependencies: Python [version — check with `python --version`]; libraries in `requirements.txt`.
- Install: `pip install -r requirements.txt`
- Run: [command — depends on the UI tool we choose]
- Test: `pytest`
- Sample data: [how to load the sample list]

## Reused work and limitations
- Libraries, starter templates, code and assets: pytest (testing). [add others as we use them]
- Known limitations: [what users should know]
