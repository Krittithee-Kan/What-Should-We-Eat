"""Small presentation adapters; application rules remain in ``app.logic``."""

PRICE_OPTIONS = {
    "Any price": None,
    "Up to ฿60": 60,
    "Up to ฿100": 100,
    "Up to ฿150": 150,
    "Up to ฿200": 200,
    "Up to ฿300": 300,
    "Up to ฿500": 500,
}

CUISINE_LABELS = {
    "thai": "Thai",
    "japanese": "Japanese",
    "chinese": "Chinese",
    "korean": "Korean",
    "western": "Western",
    "other": "Other",
}

CATEGORY_LABELS = {
    "rice": "Rice",
    "noodles": "Noodles",
    "soup": "Soup",
    "curry": "Curry",
    "sushi": "Sushi",
    "shabu": "Shabu",
    "bbq": "BBQ",
    "seafood": "Seafood",
    "salad": "Salad",
    "fast food": "Fast food",
    "snacks": "Snacks",
    "bakery": "Bakery",
    "dessert": "Dessert",
    "drinks": "Drinks",
    "other": "Other",
}


def build_filters(price_label, cuisines, categories):
    """Translate screen state to the input contract used by filter logic."""
    return {
        "max_price": PRICE_OPTIONS[price_label],
        "cuisines": list(cuisines),
        "categories": list(categories),
    }


def format_price(price):
    """Format a whole-baht menu price for display."""
    return f"฿{int(price):,}"


def display_dish_name(dish):
    """Give unnamed dishes a readable presentation-only label."""
    return dish.get("dish") or "Unnamed dish"
