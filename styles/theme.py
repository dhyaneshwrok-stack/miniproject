"""
PulseMind - Theme System
==========================

Single source of truth for colors, spacing, typography, radii, and
elevation used across the entire application. No widget or view should
hardcode a color or spacing value directly -- everything is pulled from
this module (or from ``styles/dark.qss`` which is generated to be
consistent with it).
"""

from __future__ import annotations

from dataclasses import dataclass
from PySide6.QtGui import QColor, QFont


# --------------------------------------------------------------------------
# Color palette
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Palette:
    """Application color palette (mood-board aligned, dark medical theme)."""

    # Backgrounds
    bg_primary: str = "#0B0F19"
    bg_secondary: str = "#151B26"
    bg_card: str = "#1C2431"
    bg_card_hover: str = "#212B3B"
    bg_elevated: str = "#232D3D"

    # Accents
    accent: str = "#E53935"
    accent_hover: str = "#F04438"
    accent_muted: str = "#B22222"

    # Status
    success: str = "#22C55E"
    warning: str = "#F59E0B"
    danger: str = "#E53935"
    info: str = "#5A5A63"

    # Text
    text_primary: str = "#FFFFFF"
    text_secondary: str = "#94A3B8"
    text_muted: str = "#6B7789"
    text_on_accent: str = "#FFFFFF"

    # Borders / dividers
    border: str = "#2B3445"
    border_light: str = "#323D50"

    # Overlays
    overlay: str = "rgba(11, 15, 25, 0.72)"
    shadow: str = "rgba(0, 0, 0, 0.45)"


PALETTE = Palette()


def qcolor(hex_or_rgba: str) -> QColor:
    """Convert a hex string (or 'rgba(...)' css string) into a QColor."""
    if hex_or_rgba.startswith("rgba"):
        parts = hex_or_rgba[hex_or_rgba.find("(") + 1: hex_or_rgba.find(")")]
        r, g, b, a = [p.strip() for p in parts.split(",")]
        color = QColor(int(r), int(g), int(b))
        color.setAlphaF(float(a))
        return color
    return QColor(hex_or_rgba)


# --------------------------------------------------------------------------
# Spacing scale (8pt grid, matching mood board's spacing system)
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Spacing:
    xxs: int = 4
    xs: int = 8
    sm: int = 12
    md: int = 16
    lg: int = 24
    xl: int = 32
    xxl: int = 48
    xxxl: int = 64


SPACING = Spacing()


# --------------------------------------------------------------------------
# Radii & elevation
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Radius:
    sm: int = 8
    md: int = 12
    lg: int = 16
    xl: int = 20
    pill: int = 999


RADIUS = Radius()


# --------------------------------------------------------------------------
# Typography
# --------------------------------------------------------------------------

FONT_FAMILY_PRIMARY = "Inter"
FONT_FAMILY_FALLBACK = "Segoe UI"
FONT_FAMILY_DISPLAY = "Poppins"


@dataclass(frozen=True)
class TypeScale:
    """Named font sizes (in points) forming the app's type hierarchy."""

    display: int = 32
    h1: int = 26
    h2: int = 20
    h3: int = 16
    body: int = 13
    body_small: int = 12
    caption: int = 11


TYPE_SCALE = TypeScale()


def make_font(size: int, weight: QFont.Weight = QFont.Weight.Normal,
              family: str = FONT_FAMILY_PRIMARY) -> QFont:
    """Build a QFont from the theme's type scale.

    Falls back gracefully -- Qt will substitute an available system font
    (e.g. Segoe UI on Windows) if the preferred family isn't installed.
    """
    font = QFont(family)
    font.setPointSize(size)
    font.setWeight(weight)
    return font


class Typography:
    """Convenience factory methods for commonly used text styles."""

    @staticmethod
    def display() -> QFont:
        return make_font(TYPE_SCALE.display, QFont.Weight.Bold, FONT_FAMILY_DISPLAY)

    @staticmethod
    def h1() -> QFont:
        return make_font(TYPE_SCALE.h1, QFont.Weight.Bold, FONT_FAMILY_DISPLAY)

    @staticmethod
    def h2() -> QFont:
        return make_font(TYPE_SCALE.h2, QFont.Weight.DemiBold)

    @staticmethod
    def h3() -> QFont:
        return make_font(TYPE_SCALE.h3, QFont.Weight.DemiBold)

    @staticmethod
    def body() -> QFont:
        return make_font(TYPE_SCALE.body, QFont.Weight.Normal)

    @staticmethod
    def body_medium() -> QFont:
        return make_font(TYPE_SCALE.body, QFont.Weight.Medium)

    @staticmethod
    def body_small() -> QFont:
        return make_font(TYPE_SCALE.body_small, QFont.Weight.Normal)

    @staticmethod
    def caption() -> QFont:
        return make_font(TYPE_SCALE.caption, QFont.Weight.Medium)


# --------------------------------------------------------------------------
# Animation durations (ms) -- reused by every animated widget
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Motion:
    fast: int = 120
    base: int = 200
    slow: int = 320


MOTION = Motion()
