"""
PulseMind - About Page
=========================

Phase 1 implementation of PRD Module 11. This page is fully static
metadata -- there is no future business logic to gate here.
"""

from __future__ import annotations

from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from config import APP_INFO
from styles.theme import PALETTE, SPACING, Typography
from views.base_page import BasePage
from widgets.badges import StatusBadge
from widgets.cards import InfoCard


class AboutPage(BasePage):
    page_key = "about"
    page_title = "About"
    page_subtitle = "Version, technology, and project information"

    def build(self) -> None:
        self.content_layout.addWidget(self._build_overview_card())
        self.content_layout.addWidget(self._build_tech_stack_card())
        self.content_layout.addWidget(self._build_scope_card())

    def _build_overview_card(self) -> QWidget:
        card = InfoCard(APP_INFO.name, APP_INFO.tagline)
        grid = QGridLayout()
        grid.setSpacing(SPACING.sm)
        rows = [
            ("Version", APP_INFO.version),
            ("Project Type", APP_INFO.college),
            ("Platform", "Windows Desktop"),
            ("Offline Mode", "Fully offline, no cloud dependency"),
        ]
        for r, (key, value) in enumerate(rows):
            key_label = QLabel(key)
            key_label.setFont(Typography.body_small())
            key_label.setStyleSheet(f"color: {PALETTE.text_secondary};")
            value_label = QLabel(value)
            value_label.setFont(Typography.body_medium())
            value_label.setStyleSheet(f"color: {PALETTE.text_primary};")
            grid.addWidget(key_label, r, 0)
            grid.addWidget(value_label, r, 1)
        card.body_layout().addLayout(grid)
        return card

    def _build_tech_stack_card(self) -> QWidget:
        card = InfoCard("Technology Stack")
        row = QHBoxLayout()
        row.setSpacing(SPACING.xs)
        for tech in ("Python 3.13", "PySide6", "PyQtGraph", "SQLite",
                     "Pandas", "NumPy / SciPy", "ReportLab"):
            row.addWidget(StatusBadge(tech, variant="neutral"))
        row.addStretch(1)
        card.body_layout().addLayout(row)
        return card

    def _build_scope_card(self) -> QWidget:
        card = InfoCard("Development Roadmap")
        phases = [
            ("Phase 1", "Design UI and navigation", "success"),
            ("Phase 2", "Login, dashboard, patient management", "neutral"),
            ("Phase 3", "Dataset loader and waveform viewer", "neutral"),
            ("Phase 4", "Signal processing and ECG parameters", "neutral"),
            ("Phase 5", "PDF report generation and history", "neutral"),
            ("Phase 6", "Testing, polish, packaging, docs", "neutral"),
        ]
        for label, desc, variant in phases:
            row = QHBoxLayout()
            row.setSpacing(SPACING.sm)
            row.addWidget(StatusBadge(label, variant=variant))
            desc_label = QLabel(desc)
            desc_label.setFont(Typography.body_small())
            desc_label.setStyleSheet(f"color: {PALETTE.text_secondary};")
            row.addWidget(desc_label)
            row.addStretch(1)
            card.body_layout().addLayout(row)
        return card
