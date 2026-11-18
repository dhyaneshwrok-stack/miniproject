from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

from database.database import database_manager
from styles.theme import PALETTE, SPACING, Typography
from views.base_page import BasePage
from widgets.cards import InfoCard
from widgets.inputs import highlight_text


class ReportsPage(BasePage):

    page_key = "reports"
    page_title = "Reports"
    page_subtitle = "View saved ECG analyses"

    def build(self):

        self.reports = []

        self._search_text = ""

        # ----------------------------------------------------------
        # Main responsive layout
        # ----------------------------------------------------------

        self.main_layout = QHBoxLayout()

        self.main_layout.setSpacing(
            SPACING.lg
        )

        # ----------------------------------------------------------
        # Report list
        # ----------------------------------------------------------

        list_card = InfoCard(
            "Saved ECG Reports",
            "Select a saved analysis to view its results.",
        )

        self.report_list = QListWidget()

        self.report_list.setMinimumWidth(
            220
        )

        self.report_list.setMaximumWidth(
            420
        )

        self.report_list.setMinimumHeight(
            500
        )

        self.report_list.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.report_list.itemClicked.connect(
            self._show_selected_report
        )

        list_card.body_layout().addWidget(
            self.report_list
        )

        refresh_button = QPushButton(
            "Refresh Reports"
        )

        refresh_button.setMinimumHeight(
            40
        )

        refresh_button.clicked.connect(
            self.refresh
        )

        list_card.body_layout().addWidget(
            refresh_button
        )

        self.list_card = list_card

        self.main_layout.addWidget(
            list_card,
            stretch=1,
        )

        # ----------------------------------------------------------
        # Report details
        # ----------------------------------------------------------

        self.details_card = InfoCard(
            "ECG Analysis Report",
            "Select a saved report from the left.",
        )

        self.details_layout = (
            self.details_card.body_layout()
        )

        self.empty_label = QLabel(
            "No report selected.\n\n"
            "Save an ECG analysis from the ECG Analysis page, "
            "then open it here."
        )

        self.empty_label.setWordWrap(
            True
        )

        self.empty_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            """
        )

        self.details_layout.addWidget(
            self.empty_label
        )

        self.main_layout.addWidget(
            self.details_card,
            stretch=2,
        )

        self.content_layout.addLayout(
            self.main_layout
        )

        self.refresh()

        self.update_responsive_layout()

    # ==============================================================
    # Responsive layout
    # ==============================================================

    def update_responsive_layout(self):

        if not hasattr(
            self,
            "main_layout",
        ):
            return

        if self.width() < 850:

            self.main_layout.setDirection(
                QVBoxLayout.Direction.TopToBottom
            )

            self.report_list.setMinimumWidth(
                0
            )

            self.report_list.setMaximumWidth(
                100000
            )

            self.report_list.setMinimumHeight(
                260
            )

        else:

            self.main_layout.setDirection(
                QVBoxLayout.Direction.LeftToRight
            )

            self.report_list.setMinimumWidth(
                220
            )

            self.report_list.setMaximumWidth(
                420
            )

            self.report_list.setMinimumHeight(
                500
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

    # ==============================================================
    # Refresh
    # ==============================================================

    def refresh(self):

        try:

            self.reports = list(
                database_manager.get_report_history()
            )

        except Exception as error:

            self.reports = []

            self.report_list.clear()

            self.report_list.addItem(
                QListWidgetItem(
                    "Unable to load reports"
                )
            )

            self._clear_details(
                f"Could not load saved reports:\n{error}"
            )

            return

        self._display_reports()

    # ==============================================================
    # Display reports
    # ==============================================================

    def _display_reports(self):

        self.report_list.clear()

        query = (
            self._search_text
            .strip()
            .lower()
        )

        matching_reports = []

        for report in self.reports:

            patient = str(
                report["patient"]
                or "Unknown"
            )

            patient_id = str(
                report["patient_id"]
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
                f"{patient} "
                f"{patient_id} "
                f"{file_name} "
                f"{report_id}"
            ).lower()

            if (
                query
                and query not in searchable
            ):
                continue

            matching_reports.append(
                report
            )

        if not matching_reports:

            if query:

                message = (
                    "No reports match your search."
                )

            else:

                message = (
                    "No saved ECG analyses"
                )

            item = QListWidgetItem(
                message
            )

            item.setFlags(
                Qt.ItemFlag.NoItemFlags
            )

            self.report_list.addItem(
                item
            )

            if not query:

                self._clear_details(
                    "No saved ECG analysis is available yet.\n\n"
                    "Go to ECG Analysis, analyze an ECG, "
                    "and click Save Analysis."
                )

            return

        for report in matching_reports:

            patient = (
                report["patient"]
                or "Unknown"
            )

            file_name = (
                report["file_name"]
                or "Unknown file"
            )

            created_at = (
                report["created_at"]
                or ""
            )

            item = QListWidgetItem()

            item.setData(
                Qt.ItemDataRole.UserRole,
                report["id"],
            )

            item.setText(
                f"{patient}\n"
                f"{file_name}\n"
                f"{created_at}"
            )

            self.report_list.addItem(
                item
            )

        first_item = (
            self.report_list.item(0)
        )

        if first_item is not None:

            self.report_list.setCurrentItem(
                first_item
            )

            self._show_selected_report(
                first_item
            )

    # ==============================================================
    # Search
    # ==============================================================

    def set_search_text(
        self,
        text: str,
    ):

        self._search_text = (
            text or ""
        )

        if hasattr(
            self,
            "report_list",
        ):

            self._display_reports()

    # ==============================================================
    # Show selected report
    # ==============================================================

    def _show_selected_report(
        self,
        item,
    ):

        report_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        if report_id is None:
            return

        report = database_manager.get_report(
            report_id
        )

        if report is None:

            self._clear_details(
                "The selected report could not be found."
            )

            return

        self._display_report(
            report
        )

    # ==============================================================
    # Display report
    # ==============================================================

    def _display_report(
        self,
        report,
    ):

        self._clear_details()

        patient = (
            report["patient"]
            or "Unknown"
        )

        patient_id = (
            report["patient_id"]
            or "Not provided"
        )

        file_name = (
            report["file_name"]
            or "Unknown"
        )

        created_at = (
            report["created_at"]
            or "Unknown"
        )

        # ----------------------------------------------------------
        # Information
        # ----------------------------------------------------------

        info_title = QLabel(
            "Report Information"
        )

        info_title.setFont(
            Typography.h3()
        )

        info_title.setStyleSheet(
            f"""
            color: {PALETTE.text_primary};
            """
        )

        self.details_layout.addWidget(
            info_title
        )

        self._add_value(
            "Report ID",
            str(report["id"]),
        )

        self._add_value(
            "Patient",
            patient,
        )

        self._add_value(
            "Patient ID",
            patient_id,
        )

        self._add_value(
            "Age",
            (
                str(report["age"])
                if report["age"]
                not in (None, "")
                else "Not provided"
            ),
        )

        self._add_value(
            "Gender",
            (
                str(report["gender"])
                if report["gender"]
                not in (None, "")
                else "Not provided"
            ),
        )

        self._add_value(
            "ECG File",
            file_name,
        )

        self._add_value(
            "Saved On",
            created_at,
        )

        # ----------------------------------------------------------
        # Measurements
        # ----------------------------------------------------------

        measurement_title = QLabel(
            "ECG Measurements"
        )

        measurement_title.setFont(
            Typography.h3()
        )

        measurement_title.setStyleSheet(
            f"""
            color: {PALETTE.text_primary};
            padding-top: 8px;
            """
        )

        self.details_layout.addWidget(
            measurement_title
        )

        self._add_value(
            "Sampling Rate",
            self._format_value(
                report["sample_rate"],
                "Hz",
            ),
        )

        self._add_value(
            "Duration",
            self._format_value(
                report["duration"],
                "s",
            ),
        )

        self._add_value(
            "Detected Beats",
            str(
                report["beat_count"]
                or 0
            ),
        )

        self._add_value(
            "Heart Rate",
            self._format_value(
                report["heart_rate"],
                "BPM",
            ),
        )

        self._add_value(
            "Average RR",
            self._format_value(
                report["average_rr"],
                "s",
            ),
        )

        self._add_value(
            "PR Interval",
            self._format_value(
                report["pr_ms"],
                "ms",
            ),
        )

        self._add_value(
            "QRS Duration",
            self._format_value(
                report["qrs_ms"],
                "ms",
            ),
        )

        self._add_value(
            "QT Interval",
            self._format_value(
                report["qt_ms"],
                "ms",
            ),
        )

        self._add_value(
            "QTc",
            self._format_value(
                report["qtc_ms"],
                "ms",
            ),
        )

        self._add_value(
            "Status",
            str(
                report["status"]
                or "Unknown"
            ),
        )

        # ----------------------------------------------------------
        # Findings
        # ----------------------------------------------------------

        # SQLite returns sqlite3.Row objects.
        # sqlite3.Row supports report["findings"],
        # but it does NOT support report.get("findings").
        findings_value = report["findings"]

        if findings_value is None:

            findings = []

        elif isinstance(
            findings_value,
            str,
        ):

            findings = [
                line.strip()
                for line in findings_value.splitlines()
                if line.strip()
            ]

        elif isinstance(
            findings_value,
            (list, tuple),
        ):

            findings = [
                str(item).strip()
                for item in findings_value
                if str(item).strip()
            ]

        else:

            findings = [
                str(findings_value).strip()
            ]

        if findings:

            findings_title = QLabel(
                "Findings"
            )

            findings_title.setFont(
                Typography.h3()
            )

            findings_title.setStyleSheet(
                f"""
                color: {PALETTE.text_primary};
                padding-top: 8px;
                """
            )

            self.details_layout.addWidget(
                findings_title
            )

            findings_label = QLabel(
                "\n".join(
                    f"• {item}"
                    for item in findings
                )
            )

            findings_label.setWordWrap(
                True
            )

            findings_label.setStyleSheet(
                f"""
                color: {PALETTE.text_secondary};
                """
            )

            self.details_layout.addWidget(
                findings_label
            )

        self.details_layout.addStretch(
            1
        )

    # ==============================================================
    # Value row
    # ==============================================================

    def _add_value(
        self,
        label,
        value,
    ):

        row = QHBoxLayout()

        row.setSpacing(
            SPACING.sm
        )

        name_label = QLabel(
            label
        )

        name_label.setFont(
            Typography.body_small()
        )

        name_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            """
        )

        value_label = QLabel(
            str(value)
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

        value_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        row.addWidget(
            name_label
        )

        row.addStretch(
            1
        )

        row.addWidget(
            value_label
        )

        self.details_layout.addLayout(
            row
        )

    # ==============================================================
    # Format value
    # ==============================================================

    def _format_value(
        self,
        value,
        unit,
    ):

        if value is None:

            return "Not estimated"

        try:

            return (
                f"{float(value):.2f} "
                f"{unit}"
            )

        except (
            TypeError,
            ValueError,
        ):

            return (
                f"{value} {unit}"
            )

    # ==============================================================
    # Clear details
    # ==============================================================

    def _clear_details(
        self,
        message=None,
    ):

        while self.details_layout.count():

            item = (
                self.details_layout.takeAt(
                    0
                )
            )

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

            else:

                child_layout = item.layout()

                if child_layout is not None:

                    self._clear_child_layout(
                        child_layout
                    )

        if message:

            label = QLabel(
                message
            )

            label.setWordWrap(
                True
            )

            label.setStyleSheet(
                f"""
                color: {PALETTE.text_secondary};
                """
            )

            self.details_layout.addWidget(
                label
            )

    # ==============================================================
    # Clear child layout
    # ==============================================================

    def _clear_child_layout(
        self,
        layout,
    ):

        while layout.count():

            item = (
                layout.takeAt(
                    0
                )
            )

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

            else:

                child_layout = item.layout()

                if child_layout is not None:

                    self._clear_child_layout(
                        child_layout
                    )