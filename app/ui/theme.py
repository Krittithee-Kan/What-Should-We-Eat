"""Visual tokens shared by the tkinter screens."""

COLORS = {
    "canvas": "#FFFFFF",
    "surface": "#FFFFFF",
    "surface_alt": "#FAFAFA",
    "ink": "#3D3439",
    "muted": "#675C62",
    "border": "#E6E0E3",
    "selected_border": "#777075",
    "primary": "#FFFFFF",
    "primary_hover": "#F5F5F5",
    "primary_ink": "#4C3D45",
    "primary_soft": "#FAFAFA",
    "accent": "#FFFFFF",
    "accent_ink": "#4C3D45",
    "accent_soft": "#FAFAFA",
    "focus": "#737373",
    "control": "#737373",
    "control_track": "#E5E5E5",
    "spin_button": "#FCE7F3",
    "spin_button_hover": "#FBD9E9",
    "spin_button_ink": "#6A2F48",
    "surprise_button": "#FFF9E8",
    "surprise_button_hover": "#FFF3C4",
    "surprise_button_ink": "#6B591F",
    "on_primary_muted": "#675C62",
    "white": "#FFFFFF",
}

SPACE = {
    "xs": 6,
    "sm": 10,
    "md": 16,
    "lg": 24,
    "xl": 32,
}


def font(size, weight="normal"):
    """Return a portable font tuple with sensible Thai-script fallback."""
    return ("TkDefaultFont", size, weight)
