from app.logic.filter import filter_restaurants, matching_dishes


def pick_restaurant(matches, random_number):
    if not matches:
        return None
    if not 0 <= random_number < 1:
        raise ValueError("random_number must be at least 0 and less than 1")
    index = int(random_number * len(matches))
    return matches[index]


def choose_restaurant(restaurants, filters, random_number):
    matches = filter_restaurants(restaurants, filters)
    restaurant = pick_restaurant(matches, random_number)
    if restaurant is None:
        return None, []
    return restaurant, matching_dishes(restaurant, filters)
