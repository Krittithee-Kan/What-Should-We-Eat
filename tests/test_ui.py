from app.ui.presentation import (
    build_filters,
    display_dish_name,
    format_price,
    format_price_limit,
)


def test_build_filters_with_no_active_constraints():
    assert build_filters(1000, 1000, [], []) == {
        "max_price": None,
        "cuisines": [],
        "categories": [],
    }


def test_build_filters_preserves_selected_values():
    assert build_filters(
        147.8,
        1000,
        ["thai", "japanese"],
        ["rice", "noodles"],
    ) == {
        "max_price": 147,
        "cuisines": ["thai", "japanese"],
        "categories": ["rice", "noodles"],
    }


def test_format_price_limit_tracks_the_slider():
    assert format_price_limit(147.8, 1000) == "Up to ฿147"
    assert format_price_limit(1000, 1000) == "Any price"


def test_format_price_as_whole_baht():
    assert format_price(125) == "฿125"
    assert format_price(1200) == "฿1,200"


def test_display_dish_name_has_fallback():
    assert display_dish_name({"dish": "Crab fried rice"}) == "Crab fried rice"
    assert display_dish_name({"dish": ""}) == "Unnamed dish"
