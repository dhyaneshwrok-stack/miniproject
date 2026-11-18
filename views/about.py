"""
PulseMind - About Page
======================
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from config import APP_INFO
from styles.theme import PALETTE, SPACING, Typography
from views.base_page import BasePage
from widgets.badges import StatusBadge
from widgets.cards import InfoCard


class AboutPage(BasePage):

    page_key = "about"
    page_title = "About"
    page_subtitle = (
        "Version, technology, and project information"
    )

    def build(self) -> None:

        self.content_layout.addWidget(
            self._build_overview_card()
        )

        self.content_layout.addWidget(
            self._build_tech_stack_card()
        )

        self.content_layout.addWidget(
            self._build_scope_card()
        )

        self.update_responsive_layout()

    # ==============================================================
    # Overview
    # ==============================================================

    def _build_overview_card(
        self,
    ) -> QWidget:

        card = InfoCard(
            APP_INFO.name,
            APP_INFO.tagline,
        )

        grid = QGridLayout()

        grid.setSpacing(
            SPACING.sm
        )

        rows = [
            (
                "Version",
                APP_INFO.version,
            ),
            (
                "Project Type",
                APP_INFO.college,
            ),
            (
                "Platform",
                "Windows Desktop",
            ),
            (
                "Offline Mode",
                "Fully offline, no cloud dependency",
            ),
        ]

        for row_number, (
            key,
            value,
        ) in enumerate(rows):

            key_label = QLabel(
                key
            )

            key_label.setFont(
                Typography.body_small()
            )

            key_label.setStyleSheet(
                f"""
                color: {PALETTE.text_secondary};
                """
            )

            value_label = QLabel(
                value
            )

            value_label.setFont(
                Typography.body_medium()
            )

            value_label.setStyleSheet(
                f"""
                color: {PALETTE.text_primary};
                """
            )

            value_label.setWordWrap(
                True
            )

            grid.addWidget(
                key_label,
                row_number,
                0,
            )

            grid.addWidget(
                value_label,
                row_number,
                1,
            )

        card.body_layout().addLayout(
            grid
        )

        return card

    # ==============================================================
    # Technology stack
    # ==============================================================

    def _build_tech_stack_card(
        self,
    ) -> QWidget:

        card = InfoCard(
            "Technology Stack"
        )

        self.tech_grid = QGridLayout()

        self.tech_grid.setSpacing(
            SPACING.xs
        )

        technologies = [
            "Python",
            "PySide6",
            "Matplotlib",
            "SQLite",
            "Pandas",
            "NumPy",
            "SciPy",
            "ReportLab",
        ]

        self.tech_badges = []

        for tech in technologies:

            badge = StatusBadge(
                tech,
                variant="neutral",
            )

            self.tech_badges.append(
                badge
            )

        for index, badge in enumerate(
            self.tech_badges
        ):

            row = index // 4
            column = index % 4

            self.tech_grid.addWidget(
                badge,
                row,
                column,
            )

        card.body_layout().addLayout(
            self.tech_grid
        )

        return card

    # ==============================================================
    # Roadmap
    # ==============================================================

    def _build_scope_card(
        self,
    ) -> QWidget:

        card = InfoCard(
            "Development Roadmap"
        )

        phases = [
            (
                "Phase 1",
                "Design UI and navigation",
                "success",
            ),
            (
                "Phase 2",
                "ECG dataset loading and validation",
                "success",
            ),
            (
                "Phase 3",
                "Signal processing and R-peak detection",
                "success",
            ),
            (
                "Phase 4",
                "ECG measurements and rule-based analysis",
                "success",
            ),
            (
                "Phase 5",
                "SQLite history and PDF reports",
                "success",
            ),
            (
                "Phase 6",
                "Testing, polish, packaging, docs",
                "neutral",
            ),
        ]

        self.phase_rows = []

        for label, desc, variant in phases:

            row = QHBoxLayout()

            row.setSpacing(
                SPACING.sm
            )

            badge = StatusBadge(
                label,
                variant=variant,
            )

            desc_label = QLabel(
                desc
            )

            desc_label.setFont(
                Typography.body_small()
            )

            desc_label.setStyleSheet(
                f"""
                color: {PALETTE.text_secondary};
                """
            )

            desc_label.setWordWrap(
                True
            )

            row.addWidget(
                badge
            )

            row.addWidget(
                desc_label,
                stretch=1,
            )

            card.body_layout().addLayout(
                row
            )

            self.phase_rows.append(
                row
            )

        return card

    # ==============================================================
    # Responsive layout
    # ==============================================================

    def update_responsive_layout(
        self,
    ):

        if not hasattr(
            self,
            "tech_grid",
        ):
            return

        width = self.width()

        # Remove technology badges.
        for badge in self.tech_badges:

            self.tech_grid.removeWidget(
                badge
            )

        if width < 650:

            columns = 2

        elif width < 900:

            columns = 3

        else:

            columns = 4

        for index, badge in enumerate(
            self.tech_badges
        ):

            row = index // columns
            column = index % columns

            self.tech_grid.addWidget(
                badge,
                row,
                column,
            )

        # ----------------------------------------------------------
        # Roadmap rows
        # ----------------------------------------------------------

        if hasattr(
            self,
            "phase_rows",
        ):

            if width < 650:

                for row in self.phase_rows:

                    row.setDirection(
                        QVBoxLayout.Direction.TopToBottom
                    )

            else:

                for row in self.phase_rows:

                    row.setDirection(
                        QHBoxLayout.Direction.LeftToRight
                    )

    # ==============================================================
    # Resize
    # ==============================================================

    def resizeEvent(
        self,
        event,
    ):

        super().resizeEvent(
            event
        )

        self.update_responsive_layout()