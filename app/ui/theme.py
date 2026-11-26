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
