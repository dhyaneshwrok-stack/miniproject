"""
PulseMind - Reusable Button Components
=========================================

Provides the button variants required across every page: Primary,
Secondary, Danger, and a compact IconButton used in the title bar and
top bar. All variants share a common base so hover/press states and
cursor behaviour stay consistent app-wide.
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QCursor, QIcon
from PySide6.QtWidgets import QPushButton, QGraphicsOpacityEffect

from styles.theme import PALETTE, RADIUS, SPACING, Typography


class _BaseButton(QPushButton):
    """Common plumbing shared by every button variant."""

    def __init__(self, text: str = "", icon: Optional[QIcon] = None,
                 parent=None) -> None:
        super().__init__(text, parent)
        if icon is not None:
            self.setIcon(icon)
            self.setIconSize(QSize(16, 16))
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFont(Typography.body_medium())
        self.setMinimumHeight(42)
        self.setObjectName(self.__class__.__name__)


class PrimaryButton(_BaseButton):
    """High-emphasis call-to-action button (solid accent red)."""

    def __init__(self, text: str = "", icon: Optional[QIcon] = None, parent=None):
        super().__init__(text, icon, parent)
        self.setStyleSheet(f"""
            QPushButton#PrimaryButton {{
                background-color: {PALETTE.accent};
                color: {PALETTE.text_on_accent};
                border: none;
                border-radius: {RADIUS.md}px;
                padding: {SPACING.sm}px {SPACING.lg}px;
            }}
            QPushButton#PrimaryButton:hover {{
                background-color: {PALETTE.accent_hover};
            }}
            QPushButton#PrimaryButton:pressed {{
                background-color: {PALETTE.accent_muted};
            }}
            QPushButton#PrimaryButton:disabled {{
                background-color: {PALETTE.border};
                color: {PALETTE.text_muted};
            }}
        """)


class SecondaryButton(_BaseButton):
    """Medium-emphasis button: outlined, transparent background."""

    def __init__(self, text: str = "", icon: Optional[QIcon] = None, parent=None):
        super().__init__(text, icon, parent)
        self.setStyleSheet(f"""
            QPushButton#SecondaryButton {{
                background-color: transparent;
                color: {PALETTE.text_primary};
                border: 1px solid {PALETTE.border_light};
                border-radius: {RADIUS.md}px;
                padding: {SPACING.sm}px {SPACING.lg}px;
            }}
            QPushButton#SecondaryButton:hover {{
                background-color: {PALETTE.bg_card_hover};
                border-color: {PALETTE.text_secondary};
            }}
            QPushButton#SecondaryButton:pressed {{
                background-color: {PALETTE.bg_card};
            }}
            QPushButton#SecondaryButton:disabled {{
                color: {PALETTE.text_muted};
                border-color: {PALETTE.border};
            }}
        """)


class DangerButton(_BaseButton):
    """Destructive-action button: outlined red, fills red on hover."""

    def __init__(self, text: str = "", icon: Optional[QIcon] = None, parent=None):
        super().__init__(text, icon, parent)
        self.setStyleSheet(f"""
            QPushButton#DangerButton {{
                background-color: rgba(229, 57, 53, 0.12);
                color: {PALETTE.danger};
                border: 1px solid rgba(229, 57, 53, 0.35);
                border-radius: {RADIUS.md}px;
                padding: {SPACING.sm}px {SPACING.lg}px;
            }}
            QPushButton#DangerButton:hover {{
                background-color: {PALETTE.danger};
                color: {PALETTE.text_on_accent};
            }}
            QPushButton#DangerButton:pressed {{
                background-color: {PALETTE.accent_muted};
            }}
        """)


class IconButton(QPushButton):
    """Small square button showing only an icon (title bar, top bar)."""

    def __init__(self, icon: QIcon, size: int = 36, danger_hover: bool = False,
                 parent=None) -> None:
        super().__init__(parent)
        self.setIcon(icon)
        self.setIconSize(QSize(16, 16))
        self.setFixedSize(size, size)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setObjectName("IconButton")

        hover_bg = PALETTE.danger if danger_hover else PALETTE.bg_card_hover
        hover_fg = PALETTE.text_on_accent if danger_hover else PALETTE.text_primary
        self.setStyleSheet(f"""
            QPushButton#IconButton {{
                background-color: transparent;
                border: none;
                border-radius: {RADIUS.sm}px;
            }}
            QPushButton#IconButton:hover {{
                background-color: {hover_bg};
            }}
        """)
        self._danger_hover = danger_hover
        self._hover_fg = hover_fg


def fade_in(widget, duration: int = 200) -> QGraphicsOpacityEffect:
    """Attach and return a reusable opacity effect for simple fade-ins."""
    effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(effect)
    return effect
