"""
PulseMind - History Page
===========================

Phase 1 placeholder for PRD Module 9 (Report History). Includes a
styled, empty table shell so future phases only need to populate rows.
"""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QWidget

from styles.theme import PALETTE, SPACING
from utils.icons import icon
from views.base_page import BasePage
from widgets.cards import InfoCard
from widgets.inputs import DatePicker, SearchBox
from widgets.tables import StyledTableWidget


class HistoryPage(BasePage):
    page_key = "history"
    page_title = "History"
    page_subtitle = "Search and review past ECG reports"

    def build(self) -> None:
        self.content_layout.addWidget(self._build_filters())

        table = StyledTableWidget(
            ["Report ID", "Patient", "Date", "Heart Rate", "Dataset"]
        )
        table.setMinimumHeight(360)
        table.setRowCount(0)
        self.content_layout.addWidget(table)

    def _build_filters(self) -> QWidget:
        card = InfoCard()
        row = QHBoxLayout()
        row.setSpacing(SPACING.sm)
        row.addWidget(SearchBox("Search by patient or report ID..."), stretch=1)
        row.addWidget(DatePicker())
        card.body_layout().addLayout(row)
        return card
