"""
PulseMind - Top Bar
======================

Professional top navigation strip: current page title, a UI-only
search bar, a notification placeholder, the user avatar, and today's
date.
"""

from __future__ import annotations

from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from styles.theme import PALETTE, RADIUS, SPACING, Typography
from utils.icons import icon
from widgets.buttons import IconButton
from widgets.inputs import SearchBox


class TopBar(QFrame):
    """Contextual top bar shown above every page."""

    search_changed = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("TopBar")
        self.setFixedHeight(76)
        self.setStyleSheet(f"""
            #TopBar {{
                background-color: {PALETTE.bg_primary};
                border-bottom: 1px solid {PALETTE.border};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACING.xl, SPACING.sm, SPACING.xl, SPACING.sm)
        layout.setSpacing(SPACING.md)

        title_box = QVBoxLayout()
        title_box.setSpacing(0)
        self.title_label = QLabel("Dashboard")
        self.title_label.setFont(Typography.h1())
        self.title_label.setStyleSheet(f"color: {PALETTE.text_primary};")
        self.subtitle_label = QLabel("Welcome back")
        self.subtitle_label.setFont(Typography.body_small())
        self.subtitle_label.setStyleSheet(f"color: {PALETTE.text_secondary};")
        title_box.addWidget(self.title_label)
        title_box.addWidget(self.subtitle_label)
        layout.addLayout(title_box)

        layout.addStretch(1)

        self.search_box = SearchBox("Search patients, reports...")
        self.search_box.setFixedWidth(280)
        self.search_box.field.textChanged.connect(self.search_changed.emit)
        layout.addWidget(self.search_box)

        date_label = QLabel(QDate.currentDate().toString("dddd, MMM d, yyyy"))
        date_label.setFont(Typography.body_small())
        date_label.setStyleSheet(f"""
            color: {PALETTE.text_secondary};
            background-color: {PALETTE.bg_secondary};
            border: 1px solid {PALETTE.border};
            border-radius: {RADIUS.pill}px;
            padding: 8px 14px;
        """)
        layout.addWidget(date_label)

        notif_btn = IconButton(icon("bell", color=PALETTE.text_secondary, size=18), size=40)
        layout.addWidget(notif_btn)

        avatar = QLabel("PM")
        avatar.setFixedSize(40, 40)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setFont(Typography.body_medium())
        avatar.setStyleSheet(f"""
            background-color: {PALETTE.accent};
            color: {PALETTE.text_on_accent};
            border-radius: 20px;
        """)
        layout.addWidget(avatar)

    def set_page_title(self, title: str, subtitle: str = "") -> None:
        self.title_label.setText(title)
        self.subtitle_label.setText(subtitle)
        self.subtitle_label.setVisible(bool(subtitle))
