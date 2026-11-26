import pytest

from app.logic.pick import choose_restaurant, pick_restaurant
from app.sample.restaurants import SAMPLE_RESTAURANTS


@pytest.mark.parametrize(
    ("random_number", "expected_index"),
    [(0, 0), (0.5, 9), (0.999999, 18)],
)
def test_pick_restaurant_selects_deterministic_sample_positions(
    random_number, expected_index
):
    assert (
        pick_restaurant(SAMPLE_RESTAURANTS, random_number)
        is SAMPLE_RESTAURANTS[expected_index]
    )


def test_pick_restaurant_returns_none_when_there_are_no_matches():
    assert pick_restaurant([], 0.5) is None


@pytest.mark.parametrize("random_number", [-0.001, 1])
def test_pick_restaurant_rejects_random_numbers_outside_unit_interval(
    random_number,
):
    with pytest.raises(ValueError):
        pick_restaurant(SAMPLE_RESTAURANTS, random_number)


def test_choose_restaurant_returns_a_filtered_restaurant_and_its_matching_dishes():
    restaurant, dishes = choose_restaurant(
        SAMPLE_RESTAURANTS,
        {"categories": ["noodles"]},
        0,
    )

    assert restaurant["id"] == "r1"
    assert [dish["dish"] for dish in dishes] == [
        "Hong Kong-style stir-fried noodles"
    ]


def test_choose_restaurant_returns_no_result_when_filters_match_nothing():
    assert choose_restaurant(
        SAMPLE_RESTAURANTS,
        {"categories": ["sushi"]},
        0,
    ) == (None, [])
