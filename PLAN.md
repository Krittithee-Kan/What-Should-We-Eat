# Implementation plan

## First workflow
A user adds a few restaurants, closes and reopens the app, chooses filters (price and food type), presses Choose, and sees one restaurant that matches all the filters — or a clear "no match" message.

## Steps
1. Project setup: folders, `requirements.txt`, pytest working. Check: `pytest` runs. (Krittithee)
2. Sample list in `app/sample/restaurants.py`, including noodles 50, noodles 60, rice 45. (Krittithee)
3. `filter_restaurants` + tests for the strict price rule, no match, one match and combined filters. Check: `pytest tests/test_filter.py`. (Krittithee, Third member (test))
4. `pick_restaurant` + tests using fixed random numbers and an empty list. Check: `pytest tests/test_pick.py`. (Krittithee)
5. `validate_restaurant` + tests for good and rejected input. Check: `pytest tests/test_validate.py`. (Third member)
6. Storage: load/save/add/update/delete with a JSON file + tests for reopen, rejected input and damaged files. Check: `pytest tests/test_storage.py`. (Third member)
7. Basic screens calling these functions, result shown as text. Check: manual walkthrough in EVIDENCE.md. (Frontend member)
8. Animation that lands on the picked restaurant; user feedback session; fixes. (Frontend member, reviewed by Krittithee)

## Plan review
- 2026-11-26 — Confirmed Step 7 as the current scope. The frontend will use
  Python's built-in `tkinter`, call the existing filter and pick functions, and
  leave all behaviour rules and logic modules unchanged. The first screen will
  support choosing price, cuisine and category filters, browsing the matching
  restaurants, and showing a randomly picked restaurant with its matching
  dishes.

## Progress and revisions
- 2026-11-26 — Picker UI complete: added the price slider, multi-select filters,
  filtered/surprise actions and dish-wheel animation without changing logic.
- 2026-11-26 — Web runtime complete: the Python adapter calls the existing
  filter/pick functions; JavaScript handles only DOM updates and animation.
- 2026-11-26 — Visual revision complete: finalized white primary surfaces, a
  gray slider, supporting pastel accents and native scrolling.
