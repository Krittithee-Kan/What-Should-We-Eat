def filter_restaurants(restaurants, filters):
    if filters is None:
        filters = {}

    max_price = filters.get("max_price")
    types = filters.get("types")

    matches = []
    for restaurant in restaurants:
        if max_price is not None and not restaurant["price"] < max_price:
            continue
        if types and restaurant["type"] not in types:
            continue
        matches.append(restaurant)

    return matches
