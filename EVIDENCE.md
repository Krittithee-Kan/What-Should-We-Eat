# Development evidence

## Verification

### Data and Python logic

- Sample data contains 200 restaurants and 1,784 English-named dishes.
- The 15 supported categories match `app/constants.py`.
- Five focused filter tests cover empty filters, inclusive price, cuisine,
  category, combined same-dish matching and no-match behaviour.
- Desktop and web controls call the existing Python filter/pick logic;
  JavaScript contains no filter or pick implementation.

### Picker and interface

- The slider returns a whole-baht limit or no limit at its maximum.
- Cuisine and category controls support multiple selections.
- Filtered spin, surprise and no-match paths returned expected results.
- Desktop and browser interfaces loaded successfully.
- Main surfaces are white and the slider is gray; pastel colours remain small
  accents.
- Spin uses pastel pink and Surprise uses pastel yellow; button contrast is at
  least 6.14:1.
- Browser scrolling and interaction passed; localhost returned HTTP 200.
- Text contrast is at least 6.39:1 and gray-slider contrast is 4.74:1.

## Commands and results

- `uv run --with pytest pytest -q` — 62 passed.
- `git diff --check` — passed.
- `python -m app.web` — served the app at `http://localhost:5173`.
- HTTP smoke check — page, matches, filtered spin and surprise returned 200.

## Corrections

- Duplicate JavaScript filter/pick logic and its test file were removed.
- Low-contrast colour pairs were adjusted and rechecked.
- Tests needed to be revisited due to a change in sample data size.
- Changed one rule in `README.md` as we now accept price of 0 (and above) as a valid one. Only negative value is invalid.

## Member contributions

- Krittithee Kanjanapinchote — pending.
- Siriphanaphon Sirikun — pending.
- Napat Oonsamatham — pending.

## AI use

- Tools: Codex, UI design guidance, pytest and GitHub Copilot.
- Use: presentation implementation, accessibility review and filter-test
  planning/implementation.

## Final status

Frontend verification passed. User feedback is pending.
