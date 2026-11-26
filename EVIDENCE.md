# Development evidence

## Behaviour checks

### English dataset and category list
- Behaviour being checked: translated data retains the same records and numeric
  values, while the fixed categories match the requested 15-item list.
- Expected outcome, written before test code: the dataset still contains 19
  restaurants and 266 dishes with unchanged ids, prices, cuisines and
  categories; restaurant and dish names contain no Thai letters; `CATEGORIES`
  exactly matches the requested order from rice through other.
- Test reference and command, or manual steps: `pytest`; dataset integrity script
  comparing the working tree with `HEAD`; Unicode scan of `app/ui/` and
  `app/sample/`.
- Actual result: passed. The integrity comparison found 19 restaurants and 266
  dishes with ids, prices, cuisines, categories and menu counts preserved. The
  Unicode scan found no Thai letters or digits in dataset/interface text, and
  the category-order test passed. Full suite result was 7 passed.
- Correction and rerun, if needed: machine-translated menu names were reviewed;
  awkward translations such as potato wedges, mashed potatoes, lychee tea and
  several ramen names were corrected before the final rerun.

### Frontend filter handoff
- Behaviour being checked: the screen translates selected UI controls into the
  existing filter dictionary without implementing filtering itself.
- Expected outcome, written before AI-generated test code: no price selection
  produces `None`; selected cuisine and category values are passed as lists;
  clearing the screen produces no active constraints.
- Test reference and command, or manual steps: `pytest tests/test_ui.py`
- Actual result: passed. `build_filters` produced the expected dictionary in
  both the empty and selected cases; full suite result was 5 passed.
- Correction and rerun, if needed: no correction needed.

### Frontend presentation
- Behaviour being checked: restaurant and dish data returned by existing logic
  can be displayed safely, including an unnamed dish.
- Expected outcome, written before AI-generated test code: prices are shown in
  whole baht and a missing dish name receives a readable fallback label.
- Test reference and command, or manual steps: `pytest tests/test_ui.py`
- Actual result: passed. Whole-baht formatting and the unnamed-dish fallback
  matched the written expectations; full suite result was 5 passed.
- Correction and rerun, if needed: no correction needed.

### Desktop smoke test
- Behaviour being checked: the tkinter application imports and creates its
  screen without changing any logic modules.
- Expected outcome, written before AI-generated test code: the app imports with
  only standard-library UI dependencies and `pytest` remains green.
- Test reference and command, or manual steps: `python -m app.main`; then choose
  filters, press the pick button, reset, and close the window.
- Actual result: passed. The app launched, the 19-restaurant unfiltered state
  rendered, a Thai-rice selection produced a picked result, and a
  Korean-dessert selection produced the no-match state. Visual review confirmed
  the controls and primary action remain visible at the default 1180x780 size.
- Correction and rerun, if needed: the first visual pass showed the action area
  was too tall and the macOS native button reduced primary-action contrast.
  Chips were changed to three columns and the primary action moved to a themed
  ttk style; the second visual pass confirmed both fixes.
  
### Filter Test
- Behaviour being checked: `app/logic/filter.py`: `filter_restaurants` — five focused tests covering no filters, the inclusive 60-baht limit, cuisine/category filters, same-dish combined matching, and no matches.
- Expected outcome, written before AI-generated test code: the results contain only restaurants that match with every chosen filter by ID (or none if zero match).
- Test reference and command, or manual steps: `uv run --with pytest pytest -q tests/test_filter.py`
- Actual result: 5 tests passed.
- Correction and rerun, if needed: Data was changed mid-testing, so the tests were updated to assess more new restaurants.

## Member contributions
### Krittithee Kanjanapinchote
- My technical contribution: [pending]
- References: [pending]
- What I inspected: [pending]
- My decision and reason: [pending]
- Supporting evidence: [pending]

### Siriphanaphon Sirikun
- My technical contribution: [pending]
- References: [pending]
- What I inspected: [pending]
- My decision and reason: [pending]
- Supporting evidence: [pending]

### Napat Oonsamatham
- My technical contribution: [pending]
- References: [pending]
- What I inspected: [pending]
- My decision and reason: [pending]
- Supporting evidence: [pending]

## AI use
- Tools used: Codex, ui-ux-pro-max design guidance, pytest, GitHub Copilot.
- How they helped: planned and implemented the presentation layer, checked
  accessibility and layout details, and ran repeatable UI-adapter tests. GitHub Copilot for planning and implementation for filter tests.

## User feedback
Pending.

## Checkpoint update
Frontend checkpoint complete. Command: `uv run --with pytest pytest -q`.
Result on 2026-11-26 after the English dataset/category update: 7 passed in
0.01s.

## Final status
Pending.
