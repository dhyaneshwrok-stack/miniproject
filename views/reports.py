"""
PulseMind - Reports Page
===========================

Phase 1 placeholder for PRD Module 8 (ECG Report Generator). PDF
generation and report persistence are reserved for Phase 5.
"""

from __future__ import annotations

from styles.theme import PALETTE
from utils.icons import icon
from views.base_page import BasePage
from widgets.cards import EmptyStateCard


class ReportsPage(BasePage):
    page_key = "reports"
    page_title = "Reports"
    page_subtitle = "Generate and manage ECG reports"

    def build(self) -> None:
        self.content_layout.addWidget(
            EmptyStateCard(
                icon=icon("reports", color=PALETTE.text_secondary, size=28),
                title="No Reports Generated",
                description=(
                    "Generate a report after analyzing an ECG signal to see "
                    "it listed here with patient details and a summary."
                ),
                action_text="Generate Report",
            )
        )
