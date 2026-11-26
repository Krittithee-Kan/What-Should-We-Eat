import pytest

from app.data.validate import validate_restaurant


def _valid_dish(**overrides):
    dish = {
        "dish": "Pad Thai",
        "cuisine": "thai",
        "category": "noodles",
        "price": 60,
    }
    dish.update(overrides)
    return dish


def _valid_restaurant(**overrides):
    restaurant = {
        "name": "Siam Kitchen",
        "menu": [_valid_dish()],
    }
    restaurant.update(overrides)
    return restaurant


def test_accepts_a_complete_restaurant_with_multiple_dishes():
    restaurant = _valid_restaurant(
        name="  Siam Kitchen  ",
        menu=[
            _valid_dish(),
            _valid_dish(
                dish="Chicken rice",
                cuisine="thai",
                category="rice",
                price=75,
            ),
        ],
    )

    assert validate_restaurant(restaurant) == []


def test_accepts_a_dish_without_a_name():
    for dish in (
        {"cuisine": "thai", "category": "noodles", "price": 60},
        _valid_dish(dish=None),
        _valid_dish(dish=""),
    ):
        assert validate_restaurant(_valid_restaurant(menu=[dish])) == []


@pytest.mark.parametrize("restaurant", [None, "Siam Kitchen", []])
def test_rejects_non_dictionary_restaurant_input(restaurant):
    assert validate_restaurant(restaurant) == [
        "restaurant must be a dictionary"
    ]


def test_rejects_a_missing_restaurant_name():
    restaurant = _valid_restaurant()
    del restaurant["name"]

    assert "restaurant name is required" in validate_restaurant(restaurant)


@pytest.mark.parametrize("name", [None, 42, "", " \t\n"])
def test_rejects_non_text_or_blank_restaurant_names(name):
    errors = validate_restaurant(_valid_restaurant(name=name))

    assert "restaurant name is required" in errors


def test_rejects_a_missing_menu():
    restaurant = _valid_restaurant()
    del restaurant["menu"]

    assert validate_restaurant(restaurant) == ["at least one dish is required"]


@pytest.mark.parametrize("menu", [None, {}, (), []])
def test_rejects_empty_or_non_list_menus(menu):
    assert validate_restaurant(_valid_restaurant(menu=menu)) == [
        "at least one dish is required"
    ]


def test_reports_when_a_menu_entry_is_not_a_dictionary():
    assert validate_restaurant(_valid_restaurant(menu=["Pad Thai"])) == [
        "dish 1: dish must be a dictionary"
    ]


def test_rejects_missing_cuisine_category_and_price():
    errors = validate_restaurant(
        _valid_restaurant(menu=[{"dish": "Pad Thai"}])
    )

    assert errors == [
        "dish 1: cuisine must be one of: thai, japanese, chinese, korean, western, other",
        "dish 1: category must be one of: rice, noodles, soup, curry, sushi, shabu, bbq, seafood, salad, fast food, snacks, bakery, dessert, drinks, other",
        "dish 1: price must be a whole number, 0 or more",
    ]


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        (
            "cuisine",
            "martian",
            "cuisine must be one of: thai, japanese, chinese, korean, western, other",
        ),
        (
            "category",
            "brunch",
            "category must be one of: rice, noodles, soup, curry, sushi, shabu, bbq, seafood, salad, fast food, snacks, bakery, dessert, drinks, other",
        ),
        ("dish", 123, "dish name must be text"),
    ],
)
def test_rejects_invalid_dish_fields(field, value, message):
    assert validate_restaurant(
        _valid_restaurant(menu=[_valid_dish(**{field: value})])
    ) == [f"dish 1: {message}"]


@pytest.mark.parametrize("price", [True, False, 1.5, "60", None, -1])
def test_rejects_non_integer_or_negative_prices(price):
    errors = validate_restaurant(
        _valid_restaurant(menu=[_valid_dish(price=price)])
    )

    assert "dish 1: price must be a whole number, 0 or more" in errors


def test_accepts_the_smallest_positive_whole_number_price():
    assert validate_restaurant(
        _valid_restaurant(menu=[_valid_dish(price=1)])
    ) == []


def test_rejects_a_zero_price_under_the_documented_rule():
    errors = validate_restaurant(
        _valid_restaurant(menu=[_valid_dish(price=0)])
    )

    assert errors
    assert any("price" in error for error in errors)


def test_reports_multiple_errors_with_each_dish_position():
    errors = validate_restaurant(
        _valid_restaurant(
            menu=[
                _valid_dish(cuisine="martian", price=1.5),
                "not a dish",
            ]
        )
    )

    assert errors == [
        "dish 1: cuisine must be one of: thai, japanese, chinese, korean, western, other",
        "dish 1: price must be a whole number, 0 or more",
        "dish 2: dish must be a dictionary",
    ]
