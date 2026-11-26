from app.constants import CATEGORIES


def test_categories_match_the_supported_list():
    assert CATEGORIES == [
        "rice",
        "noodles",
        "soup",
        "curry",
        "sushi",
        "shabu",
        "bbq",
        "seafood",
        "salad",
        "fast food",
        "snacks",
        "bakery",
        "dessert",
        "drinks",
        "other",
    ]
