"""
PulseMind - Input Field Components
=====================================

Search box, styled dropdown (QComboBox), and date picker used across
the top bar and future forms. UI-only in Phase 1 -- no data binding.
"""

from __future__ import annotations

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import QComboBox, QDateEdit, QHBoxLayout, QLineEdit, QWidget

from styles.theme import PALETTE, RADIUS, SPACING, Typography
from utils.icons import icon


class SearchBox(QWidget):
    """Rounded search input with a leading magnifier icon."""

    def __init__(self, placeholder: str = "Search...", parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("SearchBox")
        self.setStyleSheet(f"""
            #SearchBox {{
                background-color: {PALETTE.bg_secondary};
                border: 1px solid {PALETTE.border};
                border-radius: {RADIUS.pill}px;
            }}
            #SearchBox:hover {{
                border-color: {PALETTE.text_secondary};
            }}
        """)
        self.setFixedHeight(40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACING.sm, 0, SPACING.sm, 0)
        layout.setSpacing(SPACING.xs)

        icon_label = QWidget()
        from PySide6.QtWidgets import QLabel
        icon_label = QLabel()
        icon_label.setPixmap(icon("search", color=PALETTE.text_secondary, size=16).pixmap(16, 16))
        layout.addWidget(icon_label)

        self.field = QLineEdit()
        self.field.setPlaceholderText(placeholder)
        self.field.setFont(Typography.body())
        self.field.setFrame(False)
        self.field.setStyleSheet(f"""
            QLineEdit {{
                background: transparent;
                border: none;
                color: {PALETTE.text_primary};
            }}
        """)
        layout.addWidget(self.field, stretch=1)

    def text(self) -> str:
        return self.field.text()


class Dropdown(QComboBox):
    """Themed dropdown / select menu."""

    def __init__(self, items: list[str] | None = None, parent=None) -> None:
        super().__init__(parent)
        if items:
            self.addItems(items)
        self.setFont(Typography.body())
        self.setMinimumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QComboBox {{
                background-color: {PALETTE.bg_secondary};
                color: {PALETTE.text_primary};
                border: 1px solid {PALETTE.border};
                border-radius: {RADIUS.md}px;
                padding: 6px {SPACING.md}px;
            }}
            QComboBox:hover {{
                border-color: {PALETTE.text_secondary};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 28px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {PALETTE.bg_card};
                color: {PALETTE.text_primary};
                border: 1px solid {PALETTE.border};
                border-radius: {RADIUS.sm}px;
                selection-background-color: {PALETTE.accent};
                outline: none;
                padding: 4px;
            }}
        """)


class DatePicker(QDateEdit):
    """Themed calendar date picker."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setCalendarPopup(True)
        self.setDate(QDate.currentDate())
        self.setFont(Typography.body())
        self.setMinimumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QDateEdit {{
                background-color: {PALETTE.bg_secondary};
                color: {PALETTE.text_primary};
                border: 1px solid {PALETTE.border};
                border-radius: {RADIUS.md}px;
                padding: 6px {SPACING.md}px;
            }}
            QDateEdit:hover {{
                border-color: {PALETTE.text_secondary};
            }}
            QCalendarWidget {{
                background-color: {PALETTE.bg_card};
                color: {PALETTE.text_primary};
            }}
        """)
