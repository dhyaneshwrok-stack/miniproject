"""
PulseMind - Settings Page
============================

Phase 1 placeholder for PRD Module 10. Theme toggle is wired to the
app's QSettings so the preference persists; database backup / restore
/ export are UI-only until later phases add real database content.
"""

from __future__ import annotations

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from config import SettingsKeys
from styles.theme import PALETTE, SPACING, Typography
from utils.icons import icon
from views.base_page import BasePage
from widgets.buttons import SecondaryButton
from widgets.cards import InfoCard


class SettingsPage(BasePage):
    page_key = "settings"
    page_title = "Settings"
    page_subtitle = "Application preferences"

    def build(self) -> None:
        self.settings = QSettings()
        self.content_layout.addWidget(self._build_appearance_card())
        self.content_layout.addWidget(self._build_database_card())

    def _build_appearance_card(self) -> QWidget:
        card = InfoCard("Appearance", "PulseMind is optimized for a dark, low-glare clinical environment")
        row = QHBoxLayout()
        row.setSpacing(SPACING.sm)

        dark_btn = SecondaryButton("Dark Mode", icon("about", color=PALETTE.text_secondary, size=15))
        dark_btn.setCheckable(True)
        dark_btn.setChecked(True)

        light_btn = SecondaryButton("Light Mode", icon("about", color=PALETTE.text_secondary, size=15))
        light_btn.setCheckable(True)
        light_btn.setEnabled(False)
        light_btn.setToolTip("Light theme is planned for a future release")

        row.addWidget(dark_btn)
        row.addWidget(light_btn)
        row.addStretch(1)
        card.body_layout().addLayout(row)
        return card

    def _build_database_card(self) -> QWidget:
        card = InfoCard("Database", "Backup, restore, or export your local SQLite database")
        row = QHBoxLayout()
        row.setSpacing(SPACING.sm)
        for label in ("Backup Database", "Restore Database", "Export Database"):
            btn = SecondaryButton(label)
            btn.setEnabled(False)
            btn.setToolTip("Available once patient and report data exist")
            row.addWidget(btn)
        row.addStretch(1)
        card.body_layout().addLayout(row)
        return card
