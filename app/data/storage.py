import copy
import json
import os
import shutil
from pathlib import Path

from app.data.validate import validate_restaurant
from app.sample.restaurants import SAMPLE_RESTAURANTS

DEFAULT_PATH = Path(__file__).resolve().parents[2] / "saved" / "restaurants.json"


def load_restaurants(path=DEFAULT_PATH):
    path = Path(path)
    if not path.exists():
        return copy.deepcopy(SAMPLE_RESTAURANTS), None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        data = None

    if not isinstance(data, list):
        backup = path.with_name(path.stem + ".broken" + path.suffix)
        shutil.copyfile(path, backup)
        message = f"The save file was damaged, so the built-in list was loaded. A copy was kept as {backup.name}."
        return copy.deepcopy(SAMPLE_RESTAURANTS), message

    restaurants = []
    seen_ids = set()
    skipped = 0
    for restaurant in data:
        if validate_restaurant(restaurant) or not isinstance(restaurant.get("id"), str) or restaurant["id"] in seen_ids:
            skipped += 1
            continue
        seen_ids.add(restaurant["id"])
        restaurants.append(restaurant)

    message = None
    if skipped:
        message = f"{skipped} saved restaurant(s) were damaged and skipped."
    return restaurants, message


def save_restaurants(restaurants, path=DEFAULT_PATH):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(path.name + ".tmp")
    temp_path.write_text(json.dumps(restaurants, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temp_path, path)


def next_id(restaurants):
    numbers = []
    for restaurant in restaurants:
        restaurant_id = str(restaurant.get("id", ""))
        if restaurant_id.startswith("r") and restaurant_id[1:].isdigit():
            numbers.append(int(restaurant_id[1:]))
    return f"r{max(numbers, default=0) + 1}"


def add_restaurant(restaurants, restaurant):
    errors = validate_restaurant(restaurant)
    if errors:
        return restaurants, errors

    new_restaurant = copy.deepcopy(restaurant)
    new_restaurant["name"] = new_restaurant["name"].strip()
    new_restaurant["id"] = next_id(restaurants)
    return restaurants + [new_restaurant], []


def delete_restaurant(restaurants, restaurant_id):
    return [restaurant for restaurant in restaurants if restaurant.get("id") != restaurant_id]
