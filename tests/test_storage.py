import copy
import json

import pytest

from app.data.storage import (
    add_restaurant,
    delete_restaurant,
    load_restaurants,
    next_id,
    save_restaurants,
)
from app.sample.restaurants import SAMPLE_RESTAURANTS


def _valid_dish(**overrides):
    dish = {
        "dish": "Pad Thai",
        "cuisine": "thai",
        "category": "noodles",
        "price": 60,
    }
    dish.update(overrides)
    return dish


def _valid_restaurant(restaurant_id="r1", name="Siam Kitchen"):
    return {
        "id": restaurant_id,
        "name": name,
        "menu": [_valid_dish()],
    }


def test_missing_save_file_returns_an_independent_sample_copy(tmp_path):
    path = tmp_path / "missing" / "restaurants.json"

    restaurants, message = load_restaurants(path)

    assert restaurants == SAMPLE_RESTAURANTS
    assert message is None
    assert restaurants is not SAMPLE_RESTAURANTS
    restaurants[0]["name"] = "Changed copy"
    assert restaurants[0]["name"] != SAMPLE_RESTAURANTS[0]["name"]


def test_save_creates_parent_directories_and_reopen_preserves_utf8_json(
    tmp_path,
):
    path = tmp_path / "nested" / "save" / "restaurants.json"
    restaurants = [
        _valid_restaurant(name="Caf\u00e9 Central"),
    ]

    save_restaurants(restaurants, path)

    assert path.exists()
    assert "Caf\u00e9 Central" in path.read_text(encoding="utf-8")
    reopened, message = load_restaurants(path)
    assert reopened == restaurants
    assert message is None

# Add -> Save -> Load (Similar to Update)
def test_add_assigns_next_numeric_id_trims_name_and_persists(tmp_path):
    restaurants = [
        _valid_restaurant("r2"),
        _valid_restaurant("r10"),
        _valid_restaurant("legacy-id", "Legacy Cafe"),
    ]
    original_restaurants = copy.deepcopy(restaurants)
    new_restaurant = {
        "name": "  New Kitchen  ",
        "menu": [_valid_dish(price=0)],
    }
    original_input = copy.deepcopy(new_restaurant)

    updated, errors = add_restaurant(restaurants, new_restaurant)

    assert errors == []
    assert restaurants == original_restaurants
    assert new_restaurant == original_input
    assert updated[:-1] == restaurants
    assert updated[-1] == {
        "id": "r11",
        "name": "New Kitchen",
        "menu": [_valid_dish(price=0)],
    }

    path = tmp_path / "restaurants.json"
    save_restaurants(updated, path)
    reopened, message = load_restaurants(path)
    assert reopened == updated
    assert message is None


def test_next_id_starts_at_r1_when_no_numeric_ids_exist():
    assert next_id([_valid_restaurant("legacy-id")]) == "r1"


def test_rejected_add_returns_original_list_and_validation_errors():
    restaurants = [_valid_restaurant("r1")]
    original_restaurants = copy.deepcopy(restaurants)

    updated, errors = add_restaurant(
        restaurants,
        {"name": "  ", "menu": []},
    )

    assert updated is restaurants
    assert restaurants == original_restaurants
    assert errors == [
        "restaurant name is required",
        "at least one dish is required",
    ]


def test_delete_removes_only_the_requested_id_and_persists(tmp_path):
    restaurants = [
        _valid_restaurant("r1", "First Cafe"),
        _valid_restaurant("r2", "Second Cafe"),
        _valid_restaurant("r3", "Third Cafe"),
    ]
    path = tmp_path / "restaurants.json"
    save_restaurants(restaurants, path)
    reopened, message = load_restaurants(path)
    assert message is None

    remaining = delete_restaurant(reopened, "r2")

    assert [restaurant["id"] for restaurant in remaining] == ["r1", "r3"]
    assert [restaurant["id"] for restaurant in reopened] == ["r1", "r2", "r3"]
    assert delete_restaurant(remaining, "unknown") == remaining

    save_restaurants(remaining, path)
    persisted, message = load_restaurants(path)
    assert persisted == remaining
    assert message is None


def test_empty_json_list_loads_without_warning(tmp_path):
    path = tmp_path / "restaurants.json"
    path.write_text("[]", encoding="utf-8")

    restaurants, message = load_restaurants(path)

    assert restaurants == []
    assert message is None


def test_load_skips_invalid_entries_missing_ids_and_duplicate_ids(tmp_path):
    first = _valid_restaurant("r1", "First Cafe")
    invalid = {"id": "r-invalid", "name": " ", "menu": [_valid_dish()]}
    duplicate = _valid_restaurant("r1", "Duplicate Cafe")
    missing_id = _valid_restaurant(None, "No ID Cafe")
    last = _valid_restaurant("r2", "Last Cafe")
    path = tmp_path / "restaurants.json"
    path.write_text(
        json.dumps([first, None, invalid, duplicate, missing_id, last]),
        encoding="utf-8",
    )

    restaurants, message = load_restaurants(path)

    assert restaurants == [first, last]
    assert message == "4 saved restaurant(s) were damaged and skipped."


@pytest.mark.parametrize(
    "contents",
    [
        b"{not valid json",
        b'{"not": "a list"}',
        b"\xff",
    ],
)
def test_damaged_save_file_falls_back_and_keeps_a_backup(tmp_path, contents):
    path = tmp_path / "restaurants.json"
    backup = tmp_path / "restaurants.broken.json"
    path.write_bytes(contents)

    restaurants, message = load_restaurants(path)

    assert restaurants == SAMPLE_RESTAURANTS
    assert restaurants is not SAMPLE_RESTAURANTS
    assert message is not None
    assert "damaged" in message
    assert backup.read_bytes() == contents
