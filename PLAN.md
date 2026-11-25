# Implementation plan

## First workflow
A user adds a few restaurants, closes and reopens the app, chooses filters (price, food type, walking minutes), presses Choose, and sees one restaurant that matches all the filters — or a clear "no match" message.

## Steps
1. Project setup: folders, `requirements.txt`, pytest working. Check: `pytest` runs. (Krittithee)
2. Sample list in `app/sample/restaurants.py`, including noodles 50, noodles 60, rice 45. (Krittithee)
3. `filter_restaurants` + tests for the strict price rule, no match, one match and combined filters. Check: `pytest tests/test_filter.py`. (Krittithee)
4. `pick_restaurant` + tests using fixed random numbers and an empty list. Check: `pytest tests/test_pick.py`. (Krittithee)
5. `validate_restaurant` + tests for good and rejected input. Check: `pytest tests/test_validate.py`. (Third member)
6. Storage: load/save/add/update/delete with a JSON file + tests for reopen, rejected input and damaged files. Check: `pytest tests/test_storage.py`. (Third member)
7. Basic screens calling these functions, result shown as text. Check: manual walkthrough in EVIDENCE.md. (Frontend member)
8. Animation that lands on the picked restaurant; user feedback session; fixes. (Frontend member, reviewed by Krittithee)

## Plan review
[What you changed or confirmed in this plan, and why — your own words]

## Progress and revisions
- [date] Step 1 — [status]
