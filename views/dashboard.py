"""
PulseMind - Dashboard Page
==========================

Live dashboard connected to the SQLite database.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
) 

from database.database import database_manager
from styles.theme import PALETTE, SPACING, Typography
from utils.icons import icon
from views.base_page import BasePage
from widgets.buttons import SecondaryButton
from widgets.cards import InfoCard, StatCard
from widgets.inputs import highlight_text


class DashboardPage(BasePage):
    page_key = "dashboard"
    page_title = "Dashboard"
    page_subtitle = "Overview of your ECG workspace"

    def __init__(
        self,
        parent=None,
    ):

        self.stats_cards = []

        self.total_patients_value = None
        self.total_reports_value = None
        self.recent_reports_value = None
        self.datasets_value = None

        self._search_text = ""

        self._patients = []
        self._reports = []

        super().__init__(
            parent
        )

    # =============================================================
    # Build
    # =============================================================

    def build(self):

        self._build_stats()

        self._build_quick_actions()

        columns = QHBoxLayout()

        columns.setSpacing(
            SPACING.lg
        )

        self.recent_patients_card = (
            self._build_recent_patients()
        )

        self.recent_reports_card = (
            self._build_recent_reports()
        )

        columns.addWidget(
            self.recent_patients_card,
            stretch=1,
        )

        columns.addWidget(
            self.recent_reports_card,
            stretch=1,
        )

        self.content_layout.addLayout(
            columns
        )

        self.refresh()

    # =============================================================
    # Statistics
    # =============================================================

    def _build_stats(self):

        stats_grid = QGridLayout()

        stats_grid.setSpacing(
            SPACING.lg
        )

        self.total_patients_card = StatCard(
            title="Total Patients",
            value="0",
            icon=icon(
                "patients",
                color=PALETTE.accent,
                size=18,
            ),
            accent_color=PALETTE.accent,
            subtitle="Registered patients",
        )

        self.total_patients_value = (
            self._find_value_label(
                self.total_patients_card
            )
        )

        self.total_reports_card = StatCard(
            title="Total ECG Reports",
            value="0",
            icon=icon(
                "reports",
                color=PALETTE.success,
                size=18,
            ),
            accent_color=PALETTE.success,
            subtitle="Saved analyses",
        )

        self.total_reports_value = (
            self._find_value_label(
                self.total_reports_card
            )
        )

        self.recent_reports_stat_card = StatCard(
            title="Recent Reports",
            value="0",
            icon=icon(
                "history",
                color=PALETTE.warning,
                size=18,
            ),
            accent_color=PALETTE.warning,
            subtitle="Last 7 days",
        )

        self.recent_reports_value = (
            self._find_value_label(
                self.recent_reports_stat_card
            )
        )

        self.datasets_card = StatCard(
            title="Datasets Available",
            value="0",
            icon=icon(
                "analysis",
                color=PALETTE.text_secondary,
                size=18,
            ),
            accent_color=PALETTE.text_secondary,
            subtitle="Unique ECG files",
        )

        self.datasets_value = (
            self._find_value_label(
                self.datasets_card
            )
        )

        self.stats_cards = [
            self.total_patients_card,
            self.total_reports_card,
            self.recent_reports_stat_card,
            self.datasets_card,
        ]

        stats_grid.addWidget(
            self.total_patients_card,
            0,
            0,
        )

        stats_grid.addWidget(
            self.total_reports_card,
            0,
            1,
        )

        stats_grid.addWidget(
            self.recent_reports_stat_card,
            0,
            2,
        )

        stats_grid.addWidget(
            self.datasets_card,
            0,
            3,
        )

        self.content_layout.addLayout(
            stats_grid
        )

    # =============================================================
    # Find StatCard value
    # =============================================================

    def _find_value_label(
        self,
        card,
    ):

        labels = card.findChildren(
            QLabel
        )

        for label in labels:

            if label.font().pointSize() > 20:
                return label

        if len(labels) >= 2:
            return labels[1]

        return None

    # =============================================================
    # Set stat value
    # =============================================================

    def _set_stat_value(
        self,
        label,
        value,
    ):

        if label is not None:
            label.setText(
                str(value)
            )

    # =============================================================
    # Quick actions
    # =============================================================

    def _build_quick_actions(self):

        card = InfoCard(
            "Quick Actions",
            "Jump straight into common tasks",
        )

        row = QHBoxLayout()

        row.setSpacing(
            SPACING.sm
        )

        actions = [
            (
                "Add Patient",
                "patients",
            ),
            (
                "Load Dataset",
                "analysis",
            ),
            (
                "Generate Report",
                "reports",
            ),
            (
                "View History",
                "history",
            ),
        ]

        for label, icon_name in actions:

            button = SecondaryButton(
                label,
                icon(
                    "plus"
                    if icon_name == "patients"
                    else icon_name,
                    color=PALETTE.text_secondary,
                    size=15,
                ),
            )

            button.setEnabled(
                False
            )

            button.setToolTip(
                "Use the corresponding module "
                "from the sidebar."
            )

            row.addWidget(
                button
            )

        card.body_layout().addLayout(
            row
        )

        self.content_layout.addWidget(
            card
        )

    # =============================================================
    # Recent patients
    # =============================================================

    def _build_recent_patients(
        self,
    ):

        self.recent_patients_card = InfoCard(
            "Recent Patients",
            "Recently registered patients",
        )

        self.recent_patients_layout = (
            self.recent_patients_card.body_layout()
        )

        return self.recent_patients_card

    # =============================================================
    # Recent reports
    # =============================================================

    def _build_recent_reports(
        self,
    ):

        self.recent_reports_card = InfoCard(
            "Recent Reports",
            "Recently saved ECG analyses",
        )

        self.recent_reports_layout = (
            self.recent_reports_card.body_layout()
        )

        return self.recent_reports_card

    # =============================================================
    # Refresh
    # =============================================================

    def refresh(self):

        try:

            self._patients = list(
                database_manager.get_patients()
            )

            self._reports = list(
                database_manager.get_report_history()
            )

        except Exception as error:

            self._show_database_error(
                str(error)
            )

            return

        self._update_statistics(
            self._patients,
            self._reports,
        )

        self._update_recent_patients(
            self._patients
        )

        self._update_recent_reports(
            self._reports
        )

    # =============================================================
    # Statistics update
    # =============================================================

    def _update_statistics(
        self,
        patients,
        reports,
    ):

        total_patients = len(
            patients
        )

        total_reports = len(
            reports
        )

        unique_datasets = len(
            {
                report["file_name"]
                for report in reports
                if report["file_name"]
            }
        )

        recent_cutoff = (
            datetime.now()
            - timedelta(days=7)
        )

        recent_reports = 0

        for report in reports:

            created_at = (
                report["created_at"]
            )

            if not created_at:
                continue

            try:

                report_time = (
                    datetime.fromisoformat(
                        created_at
                    )
                )

                if (
                    report_time
                    >= recent_cutoff
                ):
                    recent_reports += 1

            except ValueError:
                continue

        self._set_stat_value(
            self.total_patients_value,
            total_patients,
        )

        self._set_stat_value(
            self.total_reports_value,
            total_reports,
        )

        self._set_stat_value(
            self.recent_reports_value,
            recent_reports,
        )

        self._set_stat_value(
            self.datasets_value,
            unique_datasets,
        )

    # =============================================================
    # Recent patients
    # =============================================================

    def _update_recent_patients(
        self,
        patients,
    ):

        self._clear_layout(
            self.recent_patients_layout
        )

        query = (
            self._search_text
            .strip()
            .lower()
        )

        visible = 0

        for patient in patients[:5]:

            name = str(
                patient["name"]
                or ""
            )

            patient_id = str(
                patient["patient_id"]
                or ""
            )

            searchable = (
                f"{name} {patient_id}"
            ).lower()

            if (
                query
                and query not in searchable
            ):
                continue

            row = self._create_patient_row(
                patient
            )

            self.recent_patients_layout.addWidget(
                row
            )

            visible += 1

        if visible == 0:

            message = (
                "No patients match your search."
                if query
                else "No patients have been added yet."
            )

            self._add_empty_message(
                self.recent_patients_layout,
                message,
            )

            return

        self.recent_patients_layout.addStretch(
            1
        )

    # =============================================================
    # Recent reports
    # =============================================================

    def _update_recent_reports(
        self,
        reports,
    ):

        self._clear_layout(
            self.recent_reports_layout
        )

        query = (
            self._search_text
            .strip()
            .lower()
        )

        visible = 0

        for report in reports[:5]:

            patient_name = str(
                report["patient"]
                or ""
            )

            file_name = str(
                report["file_name"]
                or ""
            )

            report_id = str(
                report["id"]
                or ""
            )

            searchable = (
                f"{patient_name} "
                f"{file_name} "
                f"{report_id}"
            ).lower()

            if (
                query
                and query not in searchable
            ):
                continue

            row = self._create_report_row(
                report
            )

            self.recent_reports_layout.addWidget(
                row
            )

            visible += 1

        if visible == 0:

            message = (
                "No reports match your search."
                if query
                else "No ECG reports have been saved yet."
            )

            self._add_empty_message(
                self.recent_reports_layout,
                message,
            )

            return

        self.recent_reports_layout.addStretch(
            1
        )

    # =============================================================
    # Patient row
    # =============================================================

    def _create_patient_row(
        self,
        patient,
    ):

        row = QWidget()

        layout = QVBoxLayout(
            row
        )

        layout.setContentsMargins(
            8,
            6,
            8,
            6,
        )

        layout.setSpacing(
            2
        )

        name = QLabel()

        name.setTextFormat(
            Qt.TextFormat.RichText
        )

        name.setText(
            highlight_text(
                str(
                    patient["name"]
                ),
                self._search_text,
            )
        )

        name.setFont(
            Typography.body_medium()
        )

        details = QLabel(
            f"{patient['patient_id']}   •   "
            f"Age: {patient['age']}   •   "
            f"{patient['gender']}"
        )

        details.setStyleSheet(
            f"color: {PALETTE.text_secondary};"
        )

        layout.addWidget(
            name
        )

        layout.addWidget(
            details
        )

        return row

    # =============================================================
    # Report row
    # =============================================================

    def _create_report_row(
        self,
        report,
    ):

        row = QWidget()

        layout = QVBoxLayout(
            row
        )

        layout.setContentsMargins(
            8,
            6,
            8,
            6,
        )

        layout.setSpacing(
            2
        )

        patient_name = str(
            report["patient"]
            or "Unknown"
        )

        file_name = str(
            report["file_name"]
            or "Unknown file"
        )

        status = str(
            report["status"]
            or "UNKNOWN"
        )

        heart_rate = (
            report["heart_rate"]
        )

        if heart_rate is None:

            heart_rate_text = (
                "HR: --"
            )

        else:

            heart_rate_text = (
                f"HR: {float(heart_rate):.1f} BPM"
            )

        title = QLabel()

        title.setTextFormat(
            Qt.TextFormat.RichText
        )

        title.setText(
            (
                highlight_text(
                    patient_name,
                    self._search_text,
                )
                + f"  •  {status}"
            )
        )

        title.setFont(
            Typography.body_medium()
        )

        details = QLabel(
            f"{file_name}   •   "
            f"{heart_rate_text}"
        )

        details.setStyleSheet(
            f"color: {PALETTE.text_secondary};"
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            details
        )

        return row

    # =============================================================
    # Empty message
    # =============================================================

    def _add_empty_message(
        self,
        layout,
        message,
    ):

        label = QLabel(
            message
        )

        label.setWordWrap(
            True
        )

        label.setStyleSheet(
            f"color: {PALETTE.text_secondary};"
        )

        layout.addWidget(
            label
        )

        layout.addStretch(
            1
        )

    # =============================================================
    # Clear layout
    # =============================================================

    def _clear_layout(
        self,
        layout,
    ):

        while layout.count():

            item = layout.takeAt(
                0
            )

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    # =============================================================
    # Search
    # =============================================================

    def set_search_text(
        self,
        text: str,
    ):

        self._search_text = (
            text or ""
        )

        if hasattr(
            self,
            "recent_patients_layout",
        ):

            self._update_recent_patients(
                self._patients
            )

        if hasattr(
            self,
            "recent_reports_layout",
        ):

            self._update_recent_reports(
                self._reports
            )

    # =============================================================
    # Database error
    # =============================================================

    def _show_database_error(
        self,
        error,
    ):

        self._set_stat_value(
            self.total_patients_value,
            "--",
        )

        self._set_stat_value(
            self.total_reports_value,
            "--",
        )

        self._set_stat_value(
            self.recent_reports_value,
            "--",
        )

        self._set_stat_value(
            self.datasets_value,
            "--",
        )

        self._clear_layout(
            self.recent_patients_layout
        )

        self._clear_layout(
            self.recent_reports_layout
        )

        self._add_empty_message(
            self.recent_patients_layout,
            f"Could not load dashboard data:\n{error}",
        )

        self._add_empty_message(
            self.recent_reports_layout,
            f"Could not load dashboard data:\n{error}",
        )

    # =============================================================
    # Automatic refresh
    # =============================================================  

    def showEvent(
        self,
        event,
    ):

        super().showEvent(
            event
        )

        self.refresh()