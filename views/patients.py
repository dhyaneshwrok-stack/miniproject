"""
PulseMind - Patients Page
============================

Phase 1 placeholder for PRD Module 3 (Patient Management). The search
bar, filter dropdown, and table shell are all UI-only; CRUD operations
are reserved for Phase 2.
"""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QWidget

from styles.theme import PALETTE, SPACING
from utils.icons import icon
from views.base_page import BasePage
from widgets.buttons import PrimaryButton
from widgets.cards import EmptyStateCard, InfoCard
from widgets.inputs import Dropdown, SearchBox


class PatientsPage(BasePage):
    page_key = "patients"
    page_title = "Patients"
    page_subtitle = "Manage patient records and history"

    def build(self) -> None:
        self.content_layout.addWidget(self._build_toolbar())
        self.content_layout.addWidget(
            EmptyStateCard(
                icon=icon("patients", color=PALETTE.text_secondary, size=28),
                title="No Patients Registered",
                description=(
                    "Add your first patient to start tracking ECG datasets, "
                    "reports, and history for them."
                ),
                action_text="Add Patient",
            )
        )

    def _build_toolbar(self) -> QWidget:
        card = InfoCard()
        row = QHBoxLayout()
        row.setSpacing(SPACING.sm)

        search = SearchBox("Search patients by name or ID...")
        row.addWidget(search, stretch=1)

        filter_dropdown = Dropdown(["All Genders", "Male", "Female", "Other"])
        filter_dropdown.setFixedWidth(160)
        row.addWidget(filter_dropdown)

        add_btn = PrimaryButton("Add Patient", icon("plus", color="#FFFFFF", size=15))
        add_btn.setEnabled(False)
        add_btn.setToolTip("Available once Patient Management (Phase 2) is implemented")
        row.addWidget(add_btn)

        card.body_layout().addLayout(row)
        return card
