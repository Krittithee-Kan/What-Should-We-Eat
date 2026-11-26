"""Main tkinter screen for browsing, filtering and picking a restaurant."""

import random
import tkinter as tk
from tkinter import ttk

from app.constants import CATEGORIES, CUISINES
from app.logic.filter import list_matches
from app.logic.pick import choose_restaurant, pick_restaurant
from app.sample.restaurants import SAMPLE_RESTAURANTS
from app.ui.components import (
    ChoiceChip,
    MenuWheel,
    PrimaryButton,
    ScrollableFrame,
    SecondaryButton,
)
from app.ui.presentation import (
    CATEGORY_LABELS,
    CUISINE_LABELS,
    build_dish_candidates,
    build_filters,
    display_dish_name,
    format_price,
    format_price_limit,
)
from app.ui.theme import COLORS, SPACE, font


class WhatShouldWeEatApp:
    """Desktop presentation layer over the existing filtering and pick logic."""

    def __init__(self, root, restaurants=None):
        self.root = root
        self.restaurants = restaurants if restaurants is not None else SAMPLE_RESTAURANTS
        self.cuisine_vars = {value: tk.BooleanVar(value=False) for value in CUISINES}
        self.category_vars = {value: tk.BooleanVar(value=False) for value in CATEGORIES}
        highest_price = max(
            dish["price"]
            for restaurant in self.restaurants
            for dish in restaurant.get("menu", [])
        )
        self.price_ceiling = max(100, ((highest_price + 99) // 100) * 100)
        self.price_var = tk.DoubleVar(value=self.price_ceiling)
        self.price_label_var = tk.StringVar(value="Any price")
        self.match_count_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready to pick your next meal")
        self._price_refresh_job = None

        self._configure_window()
        self._configure_styles()
        self._build_screen()
        self.refresh_matches()

    def _configure_window(self):
        self.root.title("What Should We Eat?")
        self.root.geometry("1180x780")
        self.root.minsize(880, 660)
        self.root.configure(background=COLORS["canvas"])
        self.root.bind("<Return>", lambda _event: self.spin_matches())

    def _configure_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "Price.Horizontal.TScale",
            background=COLORS["surface"],
            troughcolor=COLORS["control_track"],
            bordercolor=COLORS["border"],
            lightcolor=COLORS["control"],
            darkcolor=COLORS["control"],
            sliderlength=24,
        )
        style.configure(
            "Primary.TButton",
            background=COLORS["spin_button"],
            foreground=COLORS["spin_button_ink"],
            bordercolor=COLORS["spin_button_hover"],
            lightcolor=COLORS["spin_button"],
            darkcolor=COLORS["spin_button"],
            focuscolor=COLORS["focus"],
            focusthickness=2,
            font=font(12, "bold"),
            padding=(18, 12),
            relief="flat",
        )
        style.map(
            "Primary.TButton",
            background=[
                ("pressed", COLORS["spin_button_hover"]),
                ("active", COLORS["spin_button_hover"]),
            ],
            foreground=[("disabled", COLORS["muted"])],
            bordercolor=[("focus", COLORS["focus"])],
            lightcolor=[("focus", COLORS["focus"])],
            darkcolor=[("focus", COLORS["focus"])],
        )

    def _build_screen(self):
        shell = tk.Frame(self.root, background=COLORS["canvas"])
        shell.pack(fill="both", expand=True, padx=SPACE["xl"], pady=SPACE["lg"])
        shell.grid_columnconfigure(1, weight=1)
        shell.grid_rowconfigure(1, weight=1)

        self._build_header(shell)
        self._build_filter_panel(shell)
        self._build_results_panel(shell)

    def _build_header(self, parent):
        header = tk.Frame(parent, background=COLORS["canvas"])
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, SPACE["lg"]))
        header.grid_columnconfigure(1, weight=1)

        mark = tk.Label(
            header,
            text="WE",
            width=4,
            height=2,
            background=COLORS["accent"],
            foreground=COLORS["accent_ink"],
            font=font(12, "bold"),
        )
        mark.grid(row=0, column=0, rowspan=2, sticky="w", padx=(0, SPACE["md"]))

        tk.Label(
            header,
            text="What Should We Eat?",
            background=COLORS["canvas"],
            foreground=COLORS["ink"],
            font=font(22, "bold"),
        ).grid(row=0, column=1, sticky="sw")
        tk.Label(
            header,
            text="Make your next meal an easy decision",
            background=COLORS["canvas"],
            foreground=COLORS["muted"],
            font=font(11),
        ).grid(row=1, column=1, sticky="nw")

        dish_count = sum(len(restaurant.get("menu", [])) for restaurant in self.restaurants)
        stats = tk.Frame(header, background=COLORS["primary_soft"], padx=14, pady=10)
        stats.grid(row=0, column=2, rowspan=2, sticky="e")
        tk.Label(
            stats,
            text=f"{len(self.restaurants)} restaurants  ·  {dish_count} dishes",
            background=COLORS["primary_soft"],
            foreground=COLORS["primary_ink"],
            font=font(10, "bold"),
        ).pack()

    def _build_filter_panel(self, parent):
        panel = tk.Frame(
            parent,
            width=330,
            background=COLORS["surface"],
            highlightthickness=1,
            highlightbackground=COLORS["border"],
        )
        panel.grid(row=1, column=0, sticky="nsw", padx=(0, SPACE["lg"]))
        panel.grid_propagate(False)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(0, weight=1)

        filter_scroll = ScrollableFrame(panel, background=COLORS["surface"])
        filter_scroll.grid(row=0, column=0, sticky="nsew")
        body = tk.Frame(
            filter_scroll.content,
            background=COLORS["surface"],
            padx=SPACE["lg"],
            pady=SPACE["lg"],
        )
        body.pack(fill="x")
        body.grid_columnconfigure(0, weight=1)

        tk.Label(
            body,
            text="What are you craving?",
            background=COLORS["surface"],
            foreground=COLORS["ink"],
            font=font(17, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            body,
            text="Choose as many as you like, or leave everything open.",
            wraplength=270,
            justify="left",
            background=COLORS["surface"],
            foreground=COLORS["muted"],
            font=font(10),
        ).grid(row=1, column=0, sticky="w", pady=(5, SPACE["lg"]))

        price_header = tk.Frame(body, background=COLORS["surface"])
        price_header.grid(row=2, column=0, sticky="ew")
        price_header.grid_columnconfigure(0, weight=1)
        tk.Label(
            price_header,
            text="Maximum price",
            background=COLORS["surface"],
            foreground=COLORS["ink"],
            font=font(11, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            price_header,
            textvariable=self.price_label_var,
            background=COLORS["primary_soft"],
            foreground=COLORS["primary_ink"],
            font=font(9, "bold"),
            padx=8,
            pady=4,
        ).grid(row=0, column=1, sticky="e")

        price_control = tk.Frame(body, background=COLORS["surface"])
        price_control.grid(row=3, column=0, sticky="ew", pady=(10, SPACE["lg"]))
        price_control.grid_columnconfigure(0, weight=1)
        self.price_slider = ttk.Scale(
            price_control,
            from_=0,
            to=self.price_ceiling,
            variable=self.price_var,
            command=self._on_price_change,
            orient="horizontal",
            style="Price.Horizontal.TScale",
            cursor="hand2",
            takefocus=True,
        )
        self.price_slider.grid(row=0, column=0, columnspan=2, sticky="ew")
        tk.Label(
            price_control,
            text="฿0",
            background=COLORS["surface"],
            foreground=COLORS["muted"],
            font=font(8),
        ).grid(row=1, column=0, sticky="w", pady=(3, 0))
        tk.Label(
            price_control,
            text=f"{format_price(self.price_ceiling)}+",
            background=COLORS["surface"],
            foreground=COLORS["muted"],
            font=font(8),
        ).grid(row=1, column=1, sticky="e", pady=(3, 0))

        self._section_label(body, "Cuisine", 4)
        cuisine_grid = tk.Frame(body, background=COLORS["surface"])
        cuisine_grid.grid(row=5, column=0, sticky="ew", pady=(8, SPACE["lg"]))
        self._build_choice_grid(cuisine_grid, CUISINES, self.cuisine_vars, CUISINE_LABELS)

        self._section_label(body, "Dish type", 6)
        category_grid = tk.Frame(body, background=COLORS["surface"])
        category_grid.grid(row=7, column=0, sticky="ew", pady=(8, SPACE["lg"]))
        self._build_choice_grid(
            category_grid, CATEGORIES, self.category_vars, CATEGORY_LABELS
        )

        actions = tk.Frame(
            panel,
            background=COLORS["surface"],
            padx=SPACE["lg"],
            pady=SPACE["md"],
        )
        actions.grid(row=1, column=0, sticky="ew")
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)
        self.spin_matches_button = PrimaryButton(
            actions, text="Spin my matches", command=self.spin_matches
        )
        self.spin_matches_button.grid(
            row=0, column=0, columnspan=2, sticky="ew", pady=(0, SPACE["sm"])
        )
        self.surprise_button = SecondaryButton(
            actions, text="Surprise me", command=self.surprise_me
        )
        self.surprise_button.configure(
            background=COLORS["surprise_button"],
            foreground=COLORS["surprise_button_ink"],
            activebackground=COLORS["surprise_button_hover"],
            activeforeground=COLORS["surprise_button_ink"],
        )
        self.surprise_button.grid(
            row=1, column=0, sticky="ew", padx=(0, SPACE["sm"])
        )
        SecondaryButton(actions, text="Reset", command=self.reset_filters).grid(
            row=1, column=1, sticky="ew"
        )

    def _section_label(self, parent, text, row):
        tk.Label(
            parent,
            text=text,
            background=COLORS["surface"],
            foreground=COLORS["ink"],
            font=font(11, "bold"),
        ).grid(row=row, column=0, sticky="w")

    def _build_choice_grid(self, parent, values, variables, labels):
        columns = 3
        for column in range(columns):
            parent.grid_columnconfigure(column, weight=1, uniform="chip")
        for index, value in enumerate(values):
            column = index % columns
            ChoiceChip(
                parent,
                text=labels.get(value, value.title()),
                variable=variables[value],
                command=self.refresh_matches,
            ).grid(
                row=index // columns,
                column=column,
                sticky="ew",
                padx=(0 if column == 0 else 3, 0 if column == columns - 1 else 3),
                pady=4,
            )

    def _build_results_panel(self, parent):
        panel = tk.Frame(parent, background=COLORS["canvas"])
        panel.grid(row=1, column=1, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(2, weight=1)

        title_row = tk.Frame(panel, background=COLORS["canvas"])
        title_row.grid(row=0, column=0, sticky="ew", pady=(0, SPACE["md"]))
        title_row.grid_columnconfigure(0, weight=1)
        tk.Label(
            title_row,
            text="Matching restaurants",
            background=COLORS["canvas"],
            foreground=COLORS["ink"],
            font=font(17, "bold"),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            title_row,
            textvariable=self.match_count_var,
            background=COLORS["canvas"],
            foreground=COLORS["muted"],
            font=font(10, "bold"),
        ).grid(row=0, column=1, sticky="e")

        self.result_card = tk.Frame(
            panel,
            background=COLORS["primary"],
            padx=SPACE["lg"],
            pady=SPACE["md"],
        )
        self.result_card.grid(row=1, column=0, sticky="ew", pady=(0, SPACE["md"]))
        self.result_card.grid_columnconfigure(0, weight=1)
        self.result_eyebrow = tk.Label(
            self.result_card,
            text="Ready when you are",
            background=COLORS["primary"],
            foreground=COLORS["on_primary_muted"],
            font=font(9, "bold"),
        )
        self.result_eyebrow.grid(row=0, column=0, sticky="w")
        self.result_title = tk.Label(
            self.result_card,
            text="Set your filters, then spin for a dish",
            wraplength=430,
            justify="left",
            background=COLORS["primary"],
            foreground=COLORS["primary_ink"],
            font=font(16, "bold"),
        )
        self.result_title.grid(row=1, column=0, sticky="w", pady=(3, 2))
        self.result_detail = tk.Label(
            self.result_card,
            textvariable=self.status_var,
            wraplength=430,
            justify="left",
            background=COLORS["primary"],
            foreground=COLORS["on_primary_muted"],
            font=font(10),
        )
        self.result_detail.grid(row=2, column=0, sticky="w")

        self.menu_wheel = MenuWheel(self.result_card)
        self.menu_wheel.grid(
            row=0,
            column=1,
            rowspan=3,
            sticky="e",
            padx=(SPACE["lg"], 0),
        )

        self.restaurant_list = ScrollableFrame(panel, background=COLORS["canvas"])
        self.restaurant_list.grid(row=2, column=0, sticky="nsew")

    def current_filters(self):
        cuisines = [value for value, var in self.cuisine_vars.items() if var.get()]
        categories = [value for value, var in self.category_vars.items() if var.get()]
        return build_filters(
            self.price_var.get(), self.price_ceiling, cuisines, categories
        )

    def _on_price_change(self, value):
        max_price = float(value)
        self.price_label_var.set(format_price_limit(max_price, self.price_ceiling))
        if self._price_refresh_job is not None:
            self.root.after_cancel(self._price_refresh_job)
        self._price_refresh_job = self.root.after(80, self.refresh_matches)

    def refresh_matches(self):
        matches = list_matches(self.restaurants, self.current_filters())
        self.match_count_var.set(
            f"{len(matches)} of {len(self.restaurants)} restaurants"
        )
        self._render_restaurant_cards(matches)
        eligible_dishes = [
            display_dish_name(dish)
            for _restaurant, dishes in matches
            for dish in dishes
        ]
        self.menu_wheel.set_items(eligible_dishes)
        return matches

    def _render_restaurant_cards(self, matches):
        self.restaurant_list.clear()
        if not matches:
            empty = tk.Frame(
                self.restaurant_list.content,
                background=COLORS["surface"],
                highlightthickness=1,
                highlightbackground=COLORS["border"],
                padx=SPACE["xl"],
                pady=SPACE["xl"],
            )
            empty.pack(fill="x")
            tk.Label(
                empty,
                text="No restaurant matches every filter yet",
                background=COLORS["surface"],
                foreground=COLORS["ink"],
                font=font(13, "bold"),
            ).pack(anchor="w")
            tk.Label(
                empty,
                text="Try a higher budget or remove one of your selections.",
                background=COLORS["surface"],
                foreground=COLORS["muted"],
                font=font(10),
            ).pack(anchor="w", pady=(5, 0))
            return

        for index, (restaurant, dishes) in enumerate(matches, start=1):
            card = tk.Frame(
                self.restaurant_list.content,
                background=COLORS["surface"],
                highlightthickness=1,
                highlightbackground=COLORS["border"],
                padx=SPACE["md"],
                pady=SPACE["md"],
            )
            card.pack(fill="x", pady=(0, SPACE["sm"]))
            card.grid_columnconfigure(1, weight=1)

            number = tk.Label(
                card,
                text=f"{index:02d}",
                width=4,
                height=2,
                background=COLORS["accent_soft"],
                foreground=COLORS["accent_ink"],
                font=font(10, "bold"),
            )
            number.grid(row=0, column=0, rowspan=2, sticky="nw", padx=(0, SPACE["md"]))
            tk.Label(
                card,
                text=restaurant["name"],
                wraplength=510,
                justify="left",
                background=COLORS["surface"],
                foreground=COLORS["ink"],
                font=font(12, "bold"),
            ).grid(row=0, column=1, sticky="w")

            prices = [dish["price"] for dish in dishes]
            price_text = format_price(min(prices))
            if min(prices) != max(prices):
                price_text = f"{price_text}–{format_price(max(prices))}"
            tk.Label(
                card,
                text=f"{len(dishes)} matching dishes  ·  {price_text}",
                background=COLORS["surface"],
                foreground=COLORS["muted"],
                font=font(9),
            ).grid(row=1, column=1, sticky="w", pady=(5, 0))

    def _filtered_dish_candidates(self, filters):
        return build_dish_candidates(list_matches(self.restaurants, filters))

    def spin_matches(self):
        filters = self.current_filters()
        candidates = self._filtered_dish_candidates(filters)
        selected = pick_restaurant(candidates, random.random())
        if selected is None:
            self._show_no_match()
            return
        self._start_dish_spin(candidates, selected, "Filtered menu matches")

    def surprise_me(self):
        restaurant, dishes = choose_restaurant(
            self.restaurants, {}, random.random()
        )
        if restaurant is None:
            self._show_no_match()
            return

        candidates = [
            {"index": index, "restaurant": restaurant, "dish": dish}
            for index, dish in enumerate(dishes)
        ]
        selected = pick_restaurant(candidates, random.random())
        self._start_dish_spin(candidates, selected, "A surprise from the full list")

    def _start_dish_spin(self, candidates, selected, helper_text):
        if self.menu_wheel.spinning:
            return

        self.menu_wheel.set_items(
            [display_dish_name(candidate["dish"]) for candidate in candidates]
        )
        self._set_spin_buttons("disabled")
        self.result_eyebrow.configure(text="SPINNING THE WHEEL")
        self.result_title.configure(text="Finding your dish...")
        self.status_var.set(helper_text)

        def finish():
            self._show_dish_result(selected)
            self._set_spin_buttons("normal")

        self.menu_wheel.animate_to(selected["index"], finish)

    def _show_dish_result(self, selected):
        dish = selected["dish"]
        restaurant = selected["restaurant"]
        self.result_eyebrow.configure(text="YOUR MENU")
        self.result_title.configure(text=display_dish_name(dish))
        self.status_var.set(
            f"{restaurant['name']}  ·  {format_price(dish['price'])}"
        )

    def _show_no_match(self):
        self.menu_wheel.set_items([])
        self.result_eyebrow.configure(text="NO MENU YET")
        self.result_title.configure(text="No dish matches every filter")
        self.status_var.set("Reset one or more filters, then try again.")

    def _set_spin_buttons(self, state):
        self.spin_matches_button.configure(state=state)
        self.surprise_button.configure(state=state)

    def reset_filters(self):
        self.price_var.set(self.price_ceiling)
        self.price_label_var.set("Any price")
        if self._price_refresh_job is not None:
            self.root.after_cancel(self._price_refresh_job)
            self._price_refresh_job = None
        for variable in (*self.cuisine_vars.values(), *self.category_vars.values()):
            variable.set(False)
        self.result_eyebrow.configure(text="Ready when you are")
        self.result_title.configure(text="Set your filters, then spin for a dish")
        self.status_var.set("Ready to pick your next meal")
        self.refresh_matches()


def run():
    root = tk.Tk()
    WhatShouldWeEatApp(root)
    root.mainloop()
