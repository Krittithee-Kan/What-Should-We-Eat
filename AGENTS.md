# Repository instructions

## Project context
"What Should We Eat?" is a small Python app that keeps a saved list of restaurants and picks one restaurant from those matching the user's filters. Tests use pytest. See README.md for product details and behaviour rules.

## Relevant files
- `app/logic/filter.py`: `filter_restaurants(restaurants, filters)` — returns only the restaurants matching every chosen filter.
- `app/logic/pick.py`: `pick_restaurant(matches, random_number)` — picks one restaurant from the matches, or `None` if there are none.
- `app/data/validate.py`: `validate_restaurant(form_input)` — checks user input before saving.
- `app/data/storage.py`: load, save, add, update and delete restaurants in a JSON file.
- `app/ui/`, `app/main.py`: screens only. No filter, pick, validation or storage rules here.
- `app/sample/restaurants.py`: small sample list used by tests and demos.
- `tests/`: pytest tests, one file per part.

## Change boundaries
- Only change the files needed for the task you were given.
- Do not rename the shared functions listed above or change what they take/return without asking.
- Do not delete or weaken existing tests to make them pass.
- Keep rules (filtering, picking, validation, storage) out of the UI code.
- Do not add new libraries without asking.
- Ask before changing behaviour rules in README.md.

## Commands
- Install: `pip install -r requirements.txt`
- Run: [actual command once the UI tool is chosen]
- Test: `pytest`

## Working and review expectations
- Before coding, show a short plan; the team reviews it and records it in PLAN.md.
- Keep each change small so a person can read all of it.
- Expected test outcomes are written by the team in EVIDENCE.md first; do not invent them.
- After a change, run `pytest` and report the real result, including failures and anything you are unsure about.
- Never report a check or result that did not actually happen.
