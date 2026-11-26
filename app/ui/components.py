"""Reusable tkinter widgets used by the desktop screen."""

import math
import tkinter as tk
from tkinter import ttk

from app.ui.theme import COLORS, font


class ChoiceChip(tk.Checkbutton):
    """A compact multi-select control with an obvious selected state."""

    def __init__(self, parent, *, text, variable, command=None):
        self._label = text
        self._variable = variable
        self._command = command
        super().__init__(
            parent,
            variable=variable,
            command=self._handle_change,
            indicatoron=False,
            selectcolor=COLORS["surface"],
            background=COLORS["surface_alt"],
            foreground=COLORS["ink"],
            activebackground=COLORS["surface"],
            activeforeground=COLORS["ink"],
            disabledforeground=COLORS["muted"],
            font=font(10, "bold"),
            relief="flat",
            overrelief="flat",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground=COLORS["border"],
            highlightcolor=COLORS["focus"],
            padx=10,
            pady=8,
            cursor="hand2",
            takefocus=True,
        )
        self._variable.trace_add("write", self._sync_selected_state)
        self._sync_selected_state()

    def _handle_change(self):
        self._sync_selected_state()
        if self._command is not None:
            self._command()

    def _sync_selected_state(self, *_args):
        if self._variable.get():
            self.configure(
                text=f"✓  {self._label}",
                background=COLORS["surface"],
                activebackground=COLORS["surface"],
                highlightthickness=2,
                highlightbackground=COLORS["selected_border"],
            )
        else:
            self.configure(
                text=self._label,
                background=COLORS["surface_alt"],
                activebackground=COLORS["primary_soft"],
                highlightthickness=1,
                highlightbackground=COLORS["border"],
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
            foreground=COLORS["primary_ink"],
            activebackground=COLORS["primary_soft"],
            activeforeground=COLORS["primary_ink"],
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


class MenuWheel(tk.Canvas):
    """Decorative wheel whose final segment mirrors the selected menu item."""

    PALETTE = (
        "#F5CBD8",
        "#FFF0B8",
        "#FFE1EA",
        "#F2DF9A",
        "#EDAFC4",
        "#FFF7D6",
    )
    MAX_SEGMENTS = 24

    def __init__(self, parent, *, size=184):
        super().__init__(
            parent,
            width=size,
            height=size,
            background=COLORS["primary"],
            borderwidth=0,
            highlightthickness=0,
            takefocus=False,
        )
        self.size = size
        self.item_count = 0
        self.segment_count = 0
        self.rotation = 0.0
        self.selected_segment = None
        self.spinning = False
        self.draw()

    def set_items(self, items):
        """Update the number of eligible dishes represented by the wheel."""
        if self.spinning:
            return
        self.item_count = len(items)
        self.segment_count = min(self.item_count, self.MAX_SEGMENTS)
        self.selected_segment = None
        self.draw()

    def animate_to(self, item_index, on_complete):
        """Spin to the visual segment mapped to ``item_index``."""
        if self.spinning or not self.segment_count:
            return False

        visual_index = item_index % self.segment_count
        segment_angle = 360 / self.segment_count
        target_center = (visual_index + 0.5) * segment_angle
        delta = (90 - target_center - self.rotation) % 360 + (360 * 4)
        start_rotation = self.rotation
        frames = 52
        self.spinning = True
        self.selected_segment = None

        def step(frame):
            progress = frame / frames
            eased = 1 - math.pow(1 - progress, 3)
            self.rotation = start_rotation + (delta * eased)
            self.draw()
            if frame < frames:
                self.after(24, step, frame + 1)
                return
            self.rotation %= 360
            self.selected_segment = visual_index
            self.spinning = False
            self.draw()
            on_complete()

        step(0)
        return True

    def draw(self):
        self.delete("all")
        center = self.size / 2
        margin = 9
        bounds = (margin, margin, self.size - margin, self.size - margin)

        if not self.segment_count:
            self.create_oval(
                *bounds,
                fill=COLORS["primary_hover"],
                outline=COLORS["on_primary_muted"],
                width=2,
            )
            self.create_text(
                center,
                center,
                text="NO\nMATCHES",
                fill=COLORS["primary_ink"],
                font=font(9, "bold"),
                justify="center",
            )
            return

        segment_angle = 360 / self.segment_count
        for index in range(self.segment_count):
            selected = index == self.selected_segment
            self.create_arc(
                *bounds,
                start=self.rotation + (index * segment_angle),
                extent=segment_angle + 0.4,
                fill=self.PALETTE[index % len(self.PALETTE)],
                outline=COLORS["white"] if selected else COLORS["primary"],
                width=3 if selected else 1,
            )

        center_radius = 31
        self.create_oval(
            center - center_radius,
            center - center_radius,
            center + center_radius,
            center + center_radius,
            fill=COLORS["primary_hover"],
            outline=COLORS["white"],
            width=2,
        )
        center_text = "SPINNING" if self.spinning else f"{self.item_count}\nDISHES"
        self.create_text(
            center,
            center,
            text=center_text,
            fill=COLORS["primary_ink"],
            font=font(8, "bold"),
            justify="center",
        )

        pointer_half = 9
        self.create_polygon(
            center - pointer_half,
            2,
            center + pointer_half,
            2,
            center,
            22,
            fill=COLORS["white"],
            outline=COLORS["primary_hover"],
            width=1,
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
