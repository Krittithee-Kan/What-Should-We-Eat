from app.logic.filter import filter_restaurants
from app.sample.restaurants import SAMPLE_RESTAURANTS


def _restaurant_ids(restaurants):
    return [restaurant["id"] for restaurant in restaurants]


def _restaurant_by_id(restaurant_id):
    return next(
        restaurant
        for restaurant in SAMPLE_RESTAURANTS
        if restaurant["id"] == restaurant_id
    )


def test_filter_without_selected_filters_returns_all_restaurants():
    assert filter_restaurants(SAMPLE_RESTAURANTS, {}) == SAMPLE_RESTAURANTS
    assert filter_restaurants(SAMPLE_RESTAURANTS, None) == SAMPLE_RESTAURANTS


def test_filter_by_max_price_includes_the_limit():
    restaurant = _restaurant_by_id("r9")
    filters = {"max_price": 60, "categories": ["other"]}

    assert filter_restaurants([restaurant], filters) == [restaurant]
    assert filter_restaurants(
        [restaurant],
        {"max_price": 59, "categories": ["other"]},
    ) == []


def test_filter_by_cuisine_and_category():
    assert _restaurant_ids(
        filter_restaurants(SAMPLE_RESTAURANTS, {"cuisines": ["japanese"]})
    ) == ["r7", "r8", "r18", "r58", "r72", "r92", "r101", "r187", "r194"]

    assert _restaurant_ids(
        filter_restaurants(SAMPLE_RESTAURANTS, {"categories": ["sushi"]})
    ) == ["r8", "r18", "r58", "r72", "r101", "r187"]


def test_combined_filters_must_match_the_same_dish():
    restaurants = [_restaurant_by_id("r5"), _restaurant_by_id("r11")]
    matches = filter_restaurants(
        restaurants,
        {"cuisines": ["thai"], "categories": ["noodles"]},
    )

    assert _restaurant_ids(matches) == ["r11"]


def test_filter_with_no_matching_restaurants_returns_empty_list():
    assert filter_restaurants(
        SAMPLE_RESTAURANTS,
        {"cuisines": ["thai"], "categories": ["curry"]},
    ) == []
