from app.constants import CATEGORIES, CUISINES


def validate_dish(dish):
    if not isinstance(dish, dict):
        return ["dish must be a dictionary"]

    errors = []
    name = dish.get("dish")
    if name is not None and not isinstance(name, str):
        errors.append("dish name must be text")
    if dish.get("cuisine") not in CUISINES:
        errors.append("cuisine must be one of: " + ", ".join(CUISINES))
    if dish.get("category") not in CATEGORIES:
        errors.append("category must be one of: " + ", ".join(CATEGORIES))
    price = dish.get("price")
    if isinstance(price, bool) or not isinstance(price, int) or price < 0:
        errors.append("price must be a whole number, 0 or more")
    return errors


def validate_restaurant(restaurant):
    if not isinstance(restaurant, dict):
        return ["restaurant must be a dictionary"]

    errors = []
    name = restaurant.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append("restaurant name is required")

    menu = restaurant.get("menu")
    if not isinstance(menu, list) or not menu:
        errors.append("at least one dish is required")
        return errors

    for number, dish in enumerate(menu, start=1):
        for error in validate_dish(dish):
            errors.append(f"dish {number}: {error}")
    return errors
