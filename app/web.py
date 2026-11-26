"""Dependency-free web adapter over the existing Python application logic."""

import json
import os
import random
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from app.constants import CATEGORIES, CUISINES
from app.logic.filter import list_matches
from app.logic.pick import choose_restaurant, pick_restaurant
from app.sample.restaurants import SAMPLE_RESTAURANTS
from app.ui.presentation import (
    CATEGORY_LABELS,
    CUISINE_LABELS,
    build_dish_candidates,
    build_filters,
    display_dish_name,
    format_price,
    format_price_limit,
)


WEB_ROOT = Path(__file__).resolve().parents[1] / "web"
HOST = "127.0.0.1"


def _price_ceiling():
    highest_price = max(
        dish["price"]
        for restaurant in SAMPLE_RESTAURANTS
        for dish in restaurant["menu"]
    )
    return max(100, ((highest_price + 99) // 100) * 100)


PRICE_CEILING = _price_ceiling()


def _filters(payload):
    return build_filters(
        payload.get("max_price", PRICE_CEILING),
        PRICE_CEILING,
        payload.get("cuisines", []),
        payload.get("categories", []),
    )


def _match_response(payload):
    filters = _filters(payload)
    matches = list_matches(SAMPLE_RESTAURANTS, filters)
    items = []
    dish_count = 0

    for restaurant, dishes in matches:
        prices = [dish["price"] for dish in dishes]
        price_text = format_price(min(prices))
        if min(prices) != max(prices):
            price_text = f"{price_text}–{format_price(max(prices))}"
        items.append(
            {
                "id": restaurant["id"],
                "name": restaurant["name"],
                "meta": f"{len(dishes)} matching dishes  ·  {price_text}",
            }
        )
        dish_count += len(dishes)

    return {
        "matches": items,
        "match_count": f"{len(matches)} of {len(SAMPLE_RESTAURANTS)} restaurants",
        "dish_count": dish_count,
        "price_label": format_price_limit(
            payload.get("max_price", PRICE_CEILING), PRICE_CEILING
        ),
    }


def _selection_response(candidates, helper_text):
    selected = pick_restaurant(candidates, random.random())
    if selected is None:
        return {"candidate_count": 0, "selected": None}

    dish = selected["dish"]
    restaurant = selected["restaurant"]
    return {
        "candidate_count": len(candidates),
        "helper_text": helper_text,
        "selected": {
            "index": selected["index"],
            "dish_name": display_dish_name(dish),
            "detail": f"{restaurant['name']}  ·  {format_price(dish['price'])}",
        },
    }


def _filtered_selection_response(payload):
    matches = list_matches(SAMPLE_RESTAURANTS, _filters(payload))
    candidates = build_dish_candidates(matches)
    return _selection_response(candidates, "Filtered menu matches")


def _surprise_response():
    restaurant, dishes = choose_restaurant(
        SAMPLE_RESTAURANTS, {}, random.random()
    )
    if restaurant is None:
        return {"candidate_count": 0, "selected": None}
    candidates = [
        {"index": index, "restaurant": restaurant, "dish": dish}
        for index, dish in enumerate(dishes)
    ]
    return _selection_response(candidates, "A surprise from the full list")


def _bootstrap_response():
    dish_count = sum(
        len(restaurant["menu"]) for restaurant in SAMPLE_RESTAURANTS
    )
    return {
        "dataset_count": (
            f"{len(SAMPLE_RESTAURANTS)} restaurants  ·  {dish_count} dishes"
        ),
        "price_ceiling": PRICE_CEILING,
        "price_ceiling_label": f"{format_price(PRICE_CEILING)}+",
        "cuisines": [
            {"value": value, "label": CUISINE_LABELS.get(value, value.title())}
            for value in CUISINES
        ],
        "categories": [
            {"value": value, "label": CATEGORY_LABELS.get(value, value.title())}
            for value in CATEGORIES
        ],
    }


class WebHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_ROOT), **kwargs)

    def _send_json(self, status, payload):
        content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def _read_json(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length == 0:
            return {}
        return json.loads(self.rfile.read(content_length).decode("utf-8"))

    def do_GET(self):
        if self.path == "/api/bootstrap":
            self._send_json(200, _bootstrap_response())
            return
        super().do_GET()

    def do_POST(self):
        try:
            payload = self._read_json()
            if self.path == "/api/matches":
                response = _match_response(payload)
            elif self.path == "/api/spin":
                response = _filtered_selection_response(payload)
            elif self.path == "/api/surprise":
                response = _surprise_response()
            else:
                self._send_json(404, {"error": "Not found"})
                return
            self._send_json(200, response)
        except (TypeError, ValueError, json.JSONDecodeError) as error:
            self._send_json(400, {"error": str(error)})


def run():
    port = int(os.environ.get("PORT", "5173"))
    server = ThreadingHTTPServer((HOST, port), WebHandler)
    print(f"What Should We Eat? running at http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
