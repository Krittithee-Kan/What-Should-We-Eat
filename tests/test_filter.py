from app.logic.filter import filter_restaurants
from app.sample.restaurants import SAMPLE_RESTAURANTS


def _restaurant_ids(restaurants):
    return [restaurant["id"] for restaurant in restaurants]


def test_filter_without_selected_filters_returns_all_restaurants():
    assert filter_restaurants(SAMPLE_RESTAURANTS, {}) == SAMPLE_RESTAURANTS
    assert filter_restaurants(SAMPLE_RESTAURANTS, None) == SAMPLE_RESTAURANTS


def test_filter_by_max_price_includes_the_limit():
    assert _restaurant_ids(
        filter_restaurants(SAMPLE_RESTAURANTS, {"max_price": 60})
    ) == ["r1", "r3", "r4", "r9", "r11", "r13", "r16", "r18", "r19"]

    assert _restaurant_ids(
        filter_restaurants(SAMPLE_RESTAURANTS, {"max_price": 59})
    ) == ["r1", "r3", "r9", "r11", "r13", "r16", "r18", "r19"]


def test_filter_by_cuisine_and_category():
    assert _restaurant_ids(
        filter_restaurants(SAMPLE_RESTAURANTS, {"cuisines": ["japanese"]})
    ) == ["r2", "r8", "r18"]

    assert _restaurant_ids(
        filter_restaurants(SAMPLE_RESTAURANTS, {"categories": ["noodles"]})
    ) == ["r1", "r2", "r3", "r5", "r6", "r8", "r12", "r18"]


def test_combined_filters_must_match_the_same_dish():
    matches = filter_restaurants(
        SAMPLE_RESTAURANTS,
        {"cuisines": ["thai"], "categories": ["noodles"]},
    )

    assert _restaurant_ids(matches) == ["r3", "r6", "r18"]
    assert "r1" not in _restaurant_ids(matches)


def test_filter_with_no_matching_restaurants_returns_empty_list():
    assert filter_restaurants(
        SAMPLE_RESTAURANTS,
        {"categories": ["sushi"]},
    ) == []
