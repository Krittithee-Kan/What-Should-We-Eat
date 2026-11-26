"""Small presentation adapters; application rules remain in ``app.logic``."""

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


def build_filters(max_price, price_ceiling, cuisines, categories):
    """Translate screen state to the input contract used by filter logic."""
    effective_max = None if max_price >= price_ceiling else int(max_price)
    return {
        "max_price": effective_max,
        "cuisines": list(cuisines),
        "categories": list(categories),
    }


def format_price_limit(max_price, price_ceiling):
    """Describe the current maximum-price slider position."""
    if max_price >= price_ceiling:
        return "Any price"
    return f"Up to {format_price(max_price)}"


def format_price(price):
    """Format a whole-baht menu price for display."""
    return f"฿{int(price):,}"


def display_dish_name(dish):
    """Give unnamed dishes a readable presentation-only label."""
    return dish.get("dish") or "Unnamed dish"


def build_dish_candidates(matches):
    """Flatten Python match results for the shared dish-wheel presentation."""
    candidates = []
    for restaurant, dishes in matches:
        for dish in dishes:
            candidates.append(
                {
                    "index": len(candidates),
                    "restaurant": restaurant,
                    "dish": dish,
                }
            )
    return candidates
