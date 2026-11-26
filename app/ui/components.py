"""Reusable tkinter widgets used by the desktop screen."""

import tkinter as tk
from tkinter import ttk

from app.ui.theme import COLORS, font


class ChoiceChip(tk.Checkbutton):
    """A compact multi-select control with an obvious selected state."""

    def __init__(self, parent, *, text, variable, command=None):
        super().__init__(
            parent,
            text=text,
            variable=variable,
            command=command,
            indicatoron=False,
            selectcolor=COLORS["primary"],
            background=COLORS["surface_alt"],
            foreground=COLORS["ink"],
            activebackground=COLORS["primary_soft"],
            activeforeground=COLORS["ink"],
            disabledforeground=COLORS["muted"],
            font=font(11, "bold"),
            relief="flat",
            overrelief="flat",
            borderwidth=0,
            highlightthickness=2,
            highlightbackground=COLORS["surface"],
            highlightcolor=COLORS["focus"],
            padx=13,
            pady=9,
            cursor="hand2",
            takefocus=True,
        )


class PrimaryButton(ttk.Button):
    """Main action button with a consistent 48px-ish touch target."""

    def __init__(self, parent, *, text, command):
        super().__init__(
            parent,
            text=text,
            command=command,
            style="Primary.TButton",
            cursor="hand2",
            takefocus=True,
        )


class SecondaryButton(tk.Button):
    """Low-emphasis action button."""

    def __init__(self, parent, *, text, command):
        super().__init__(
            parent,
            text=text,
            command=command,
            background=COLORS["surface"],
            foreground=COLORS["primary"],
            activebackground=COLORS["primary_soft"],
            activeforeground=COLORS["primary"],
            font=font(11, "bold"),
            relief="solid",
            borderwidth=1,
            highlightthickness=2,
            highlightbackground=COLORS["surface"],
            highlightcolor=COLORS["focus"],
            padx=14,
            pady=10,
            cursor="hand2",
            takefocus=True,
        )


class ScrollableFrame(tk.Frame):
    """A vertically scrollable frame that expands cards to available width."""

    def __init__(self, parent, *, background):
        super().__init__(parent, background=background)
        self.canvas = tk.Canvas(
            self,
            background=background,
            borderwidth=0,
            highlightthickness=0,
        )
        scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
            relief="flat",
            borderwidth=0,
        )
        self.content = tk.Frame(self.canvas, background=background)
        self._window = self.canvas.create_window(
            (0, 0), window=self.content, anchor="nw"
        )

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.content.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._match_content_width)
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    def _update_scroll_region(self, _event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _match_content_width(self, event):
        self.canvas.itemconfigure(self._window, width=event.width)

    def _bind_mousewheel(self, _event=None):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self, _event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        if getattr(event, "num", None) == 4:
            units = -1
        elif getattr(event, "num", None) == 5:
            units = 1
        else:
            units = -1 if event.delta > 0 else 1
        self.canvas.yview_scroll(units, "units")

    def clear(self):
        for child in self.content.winfo_children():
            child.destroy()
        self.canvas.yview_moveto(0)
