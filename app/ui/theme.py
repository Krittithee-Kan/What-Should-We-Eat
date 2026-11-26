"""Visual tokens shared by the tkinter screens."""

COLORS = {
    "canvas": "#F6F2E9",
    "surface": "#FFFDF8",
    "surface_alt": "#EEE8DC",
    "ink": "#1D2922",
    "muted": "#667168",
    "border": "#DCD5C8",
    "primary": "#28533C",
    "primary_hover": "#1E432F",
    "primary_soft": "#E0EBE2",
    "accent": "#C54B32",
    "accent_soft": "#F5DED7",
    "focus": "#A73B27",
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
