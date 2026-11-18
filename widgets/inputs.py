"""
PulseMind - Input Field Components
==================================

Search box, dropdown and date picker.
"""

from __future__ import annotations

import html

from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QWidget,
)

from styles.theme import PALETTE, RADIUS, SPACING, Typography
from utils.icons import icon


def highlight_text(
    text: str,
    query: str,
) -> str:

    safe_text = html.escape(
        str(text)
    )

    query = query.strip()

    if not query:

        return safe_text

    safe_query = html.escape(
        query
    )

    lower_text = safe_text.lower()

    lower_query = safe_query.lower()

    result = []

    start = 0

    while True:

        index = lower_text.find(
            lower_query,
            start,
        )

        if index == -1:

            result.append(
                safe_text[start:]
            )

            break

        result.append(
            safe_text[
                start:index
            ]
        )

        matched = safe_text[
            index:index
            + len(safe_query)
        ]

        result.append(
            f"""
            <span style="
                background-color: #7C3AED;
                color: white;
                padding: 1px 3px;
                border-radius: 3px;
            ">
                {matched}
            </span>
            """
        )

        start = (
            index
            + len(safe_query)
        )

    return "".join(
        result
    )


class SearchBox(QWidget):

    def __init__(
        self,
        placeholder: str = "Search...",
        parent=None,
    ) -> None:

        super().__init__(
            parent
        )

        self.setObjectName(
            "SearchBox"
        )

        self.setFixedHeight(
            40
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.setStyleSheet(
            f"""
            #SearchBox {{
                background-color: {PALETTE.bg_secondary};
                border: 1px solid {PALETTE.border};
                border-radius: {RADIUS.pill}px;
            }}

            #SearchBox:hover {{
                border-color: {PALETTE.text_secondary};
            }}
            """
        )

        layout = QHBoxLayout(
            self
        )

        layout.setContentsMargins(
            SPACING.sm,
            0,
            SPACING.sm,
            0,
        )

        layout.setSpacing(
            SPACING.xs
        )

        icon_label = QLabel()

        icon_label.setPixmap(
            icon(
                "search",
                color=PALETTE.text_secondary,
                size=16,
            ).pixmap(
                16,
                16,
            )
        )

        layout.addWidget(
            icon_label
        )

        self.field = QLineEdit()

        self.field.setPlaceholderText(
            placeholder
        )

        self.field.setFont(
            Typography.body()
        )

        self.field.setFrame(
            False
        )

        self.field.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.field.setStyleSheet(
            f"""
            QLineEdit {{
                background: transparent;
                border: none;
                color: {PALETTE.text_primary};
            }}
            """
        )

        layout.addWidget(
            self.field,
            stretch=1,
        )

    def text(
        self,
    ) -> str:

        return self.field.text()


class Dropdown(QComboBox):

    def __init__(
        self,
        items: list[str] | None = None,
        parent=None,
    ) -> None:

        super().__init__(
            parent
        )

        if items:

            self.addItems(
                items
            )

        self.setFont(
            Typography.body()
        )

        self.setMinimumHeight(
            40
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.setStyleSheet(
            f"""
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
            """
        )


class DatePicker(QDateEdit):

    def __init__(
        self,
        parent=None,
    ) -> None:

        super().__init__(
            parent
        )

        self.setCalendarPopup(
            True
        )

        self.setDate(
            QDate.currentDate()
        )

        self.setFont(
            Typography.body()
        )

        self.setMinimumHeight(
            40
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.setStyleSheet(
            f"""
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

            QDateEdit::drop-down {{
                border: none;
                width: 28px;
            }}

            QCalendarWidget {{
                background-color: {PALETTE.bg_card};
                color: {PALETTE.text_primary};
            }}
            """
        )