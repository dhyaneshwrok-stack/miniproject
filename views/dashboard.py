"""
PulseMind - Dashboard Page
=============================

Phase 1 placeholder for PRD Module 2. Displays the intended layout
(summary stats, quick actions, recent activity) with static placeholder
data -- no database reads yet.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from styles.theme import PALETTE, SPACING, Typography
from utils.icons import icon
from views.base_page import BasePage
from widgets.buttons import SecondaryButton
from widgets.cards import EmptyStateCard, InfoCard, StatCard


class DashboardPage(BasePage):
    page_key = "dashboard"
    page_title = "Dashboard"
    page_subtitle = "Overview of your ECG workspace"

    def build(self) -> None:
        stats_grid = QGridLayout()
        stats_grid.setSpacing(SPACING.lg)

        stats = [
            ("Total Patients", "0", "patients", PALETTE.accent),
            ("Total ECG Reports", "0", "reports", PALETTE.success),
            ("Recent Reports", "0", "history", PALETTE.warning),
            ("Datasets Available", "0", "analysis", PALETTE.text_secondary),
        ]
        for column, (title, value, icon_name, color) in enumerate(stats):
            card = StatCard(
                title=title,
                value=value,
                icon=icon(icon_name, color=color, size=18),
                accent_color=color,
                subtitle="No data yet",
            )
            stats_grid.addWidget(card, 0, column)
        self.content_layout.addLayout(stats_grid)

        self.content_layout.addWidget(self._build_quick_actions())

        columns = QHBoxLayout()
        columns.setSpacing(SPACING.lg)
        columns.addWidget(self._build_recent_patients(), stretch=1)
        columns.addWidget(self._build_recent_reports(), stretch=1)
        self.content_layout.addLayout(columns)

    def _build_quick_actions(self) -> QWidget:
        card = InfoCard("Quick Actions", "Jump straight into common tasks")
        row = QHBoxLayout()
        row.setSpacing(SPACING.sm)
        actions = [
            ("Add Patient", "patients"),
            ("Load Dataset", "analysis"),
            ("Generate Report", "reports"),
            ("View History", "history"),
        ]
        for label, icon_name in actions:
            btn = SecondaryButton(label, icon("plus" if icon_name == "patients" else icon_name,
                                                color=PALETTE.text_secondary, size=15))
            btn.setEnabled(False)
            btn.setToolTip("Available once this module is implemented")
            row.addWidget(btn)
        card.body_layout().addLayout(row)
        return card

    def _build_recent_patients(self) -> QWidget:
        return EmptyStateCard(
            icon=icon("patients", color=PALETTE.text_secondary, size=26),
            title="No Patients Yet",
            description="Patients you add will appear here with a quick summary of their most recent ECG activity.",
        )

    def _build_recent_reports(self) -> QWidget:
        return EmptyStateCard(
            icon=icon("reports", color=PALETTE.text_secondary, size=26),
            title="No Reports Yet",
            description="Generated ECG reports will be listed here for quick access and re-printing.",
        )
