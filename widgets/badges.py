"""
PulseMind - Status Badges
===========================

Small pill-shaped status labels (e.g. "Active", "Pending", "Error")
used inside tables and cards throughout the application.
"""

from __future__ import annotations

from PySide6.QtWidgets import QLabel

from styles.theme import PALETTE, RADIUS, Typography


class StatusBadge(QLabel):
    """Pill-shaped label communicating status via color, not just text."""

    VARIANTS = {
        "success": PALETTE.success,
        "warning": PALETTE.warning,
        "danger": PALETTE.danger,
        "neutral": PALETTE.text_secondary,
        "info": PALETTE.text_secondary,
    }

    def __init__(self, text: str, variant: str = "neutral", parent=None) -> None:
        super().__init__(text, parent)
        self.setFont(Typography.caption())
        self.set_variant(variant)

    def set_variant(self, variant: str) -> None:
        color = self.VARIANTS.get(variant, PALETTE.text_secondary)
        self.setStyleSheet(f"""
            QLabel {{
                color: {color};
                background-color: rgba(148, 163, 184, 0.12);
                border: 1px solid {color};
                border-radius: {RADIUS.pill}px;
                padding: 3px 10px;
            }}
        """)
        self.setStyleSheet(self.styleSheet().replace(
            "rgba(148, 163, 184, 0.12)", self._tint(color)
        ))

    @staticmethod
    def _tint(hex_color: str) -> str:
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            return "rgba(148, 163, 184, 0.12)"
        r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        return f"rgba({r}, {g}, {b}, 0.14)"
