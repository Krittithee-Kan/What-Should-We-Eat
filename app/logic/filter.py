def dish_matches(dish, filters):
    max_price = filters.get("max_price")
    cuisines = filters.get("cuisines")
    categories = filters.get("categories")

    if max_price is not None and not dish["price"] <= max_price:
        return False
    if cuisines and dish["cuisine"] not in cuisines:
        return False
    if categories and dish["category"] not in categories:
        return False
    return True


def matching_dishes(restaurant, filters):
    if filters is None:
        filters = {}
    return [dish for dish in restaurant["menu"] if dish_matches(dish, filters)]


def filter_restaurants(restaurants, filters):
    if filters is None:
        filters = {}

    matches = []
    for restaurant in restaurants:
        if matching_dishes(restaurant, filters):
            matches.append(restaurant)

    return matches


def list_matches(restaurants, filters):
    if filters is None:
        filters = {}

    results = []
    for restaurant in restaurants:
        dishes = matching_dishes(restaurant, filters)
        if dishes:
            results.append((restaurant, dishes))

    return results
