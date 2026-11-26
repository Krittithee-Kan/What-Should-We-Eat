from app.ui.presentation import build_filters, display_dish_name, format_price


def test_build_filters_with_no_active_constraints():
    assert build_filters("Any price", [], []) == {
        "max_price": None,
        "cuisines": [],
        "categories": [],
    }


def test_build_filters_preserves_selected_values():
    assert build_filters("Up to ฿150", ["thai"], ["rice", "noodles"]) == {
        "max_price": 150,
        "cuisines": ["thai"],
        "categories": ["rice", "noodles"],
    }


def test_format_price_as_whole_baht():
    assert format_price(125) == "฿125"
    assert format_price(1200) == "฿1,200"


def test_display_dish_name_has_fallback():
    assert display_dish_name({"dish": "Crab fried rice"}) == "Crab fried rice"
    assert display_dish_name({"dish": ""}) == "Unnamed dish"
