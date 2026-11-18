from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from database.database import database_manager
from styles.theme import PALETTE, SPACING
from views.base_page import BasePage
from widgets.cards import InfoCard
from widgets.inputs import DatePicker, SearchBox
from widgets.tables import StyledTableWidget


class HistoryPage(BasePage):

    page_key = "history"
    page_title = "History"
    page_subtitle = "Search and review past ECG analyses"

    def build(self):

        self._search_text = ""
        self._history_rows = []

        # -----------------------------------------------------
        # Search and date filters
        # -----------------------------------------------------

        self.content_layout.addWidget(
            self._build_filters()
        )

        # -----------------------------------------------------
        # History table
        # -----------------------------------------------------

        self.table = StyledTableWidget(
            [
                "Report ID",
                "Patient",
                "Age",
                "Gender",
                "Date",
                "Heart Rate",
                "Dataset",
                "Status",
            ]
        )

        self.table.setMinimumHeight(360)

        self.content_layout.addWidget(
            self.table
        )

        # -----------------------------------------------------
        # Result message
        # -----------------------------------------------------

        self.message_label = QLabel(
            "Loading analysis history..."
        )

        self.message_label.setWordWrap(True)

        self.message_label.setStyleSheet(
            f"color: {PALETTE.text_secondary}; padding: 6px;"
        )

        self.content_layout.addWidget(
            self.message_label
        )

        self.refresh()
        self.update_responsive_layout()

    # =========================================================
    # Filters
    # =========================================================

    def _build_filters(self):

        card = InfoCard()

        self.filters_layout = QHBoxLayout()
        self.filters_layout.setSpacing(SPACING.sm)

        self.search_box = SearchBox(
            "Search patient, report ID, filename or status..."
        )

        self.search_box.field.textChanged.connect(
            self._filter_rows
        )

        self.filters_layout.addWidget(
            self.search_box,
            stretch=1,
        )

        self.date_picker = DatePicker()

        self.filters_layout.addWidget(
            self.date_picker
        )

        card.body_layout().addLayout(
            self.filters_layout
        )

        return card

    # =========================================================
    # Responsive layout
    # =========================================================

    def update_responsive_layout(self):

        if not hasattr(self, "filters_layout"):
            return

        if self.width() < 650:
            self.filters_layout.setDirection(
                QVBoxLayout.Direction.TopToBottom
            )
        else:
            self.filters_layout.setDirection(
                QHBoxLayout.Direction.LeftToRight
            )

    def resizeEvent(self, event):

        super().resizeEvent(event)
        self.update_responsive_layout()

    # =========================================================
    # Refresh history
    # =========================================================

    def refresh(self):

        try:
            self._history_rows = database_manager.get_history()

        except Exception as error:
            self._history_rows = []

            self.message_label.setText(
                f"Could not load history: {error}"
            )

        self._fill_table()

    # =========================================================
    # Safe database value helper
    # =========================================================

    @staticmethod
    def _get_value(row, key, default=None):

        try:
            return row[key]
        except (KeyError, IndexError, TypeError):
            return default

    # =========================================================
    # Fill and filter history table
    # =========================================================

    def _fill_table(self):

        rows = self._history_rows
        query = self._search_text.strip().lower()

        self.table.setRowCount(0)

        visible_count = 0

        for row in rows:

            report_id = self._get_value(row, "id", "")
            patient = self._get_value(row, "patient", "Unknown")
            age = self._get_value(row, "age", "")
            gender = self._get_value(row, "gender", "")
            created_at = self._get_value(row, "created_at", "")
            heart_rate = self._get_value(row, "heart_rate")
            file_name = self._get_value(row, "file_name", "")
            status = str(
                self._get_value(row, "status", "UNKNOWN") or "UNKNOWN"
            ).upper()

            # -------------------------------------------------
            # Format values for display
            # -------------------------------------------------

            if heart_rate is None:
                heart_rate_text = "—"
            else:
                try:
                    heart_rate_text = f"{float(heart_rate):.1f} BPM"
                except (TypeError, ValueError):
                    heart_rate_text = str(heart_rate)

            values = [
                str(report_id),
                str(patient or "Unknown"),
                str(age) if age not in (None, "") else "—",
                str(gender) if gender else "—",
                str(created_at or ""),
                heart_rate_text,
                str(file_name or ""),
                status,
            ]

            # -------------------------------------------------
            # Search across all visible table fields
            # -------------------------------------------------

            searchable_text = " ".join(values).lower()

            if query and query not in searchable_text:
                continue

            table_row = self.table.rowCount()
            self.table.insertRow(table_row)

            visible_count += 1

            for column, value in enumerate(values):

                item = QTableWidgetItem(value)

                item.setFlags(
                    item.flags()
                    & ~Qt.ItemFlag.ItemIsEditable
                )

                # Highlight search matches.
                if query and query in value.lower():
                    item.setBackground(
                        QColor("#7C3AED")
                    )
                    item.setForeground(
                        QColor("#FFFFFF")
                    )

                # Give the status cell a clear visual label.
                if column == 7:

                    if status == "NORMAL":
                        item.setBackground(
                            QColor("#14532D")
                        )
                        item.setForeground(
                            QColor("#BBF7D0")
                        )

                    elif status == "FLAGGED":
                        item.setBackground(
                            QColor("#7F1D1D")
                        )
                        item.setForeground(
                            QColor("#FECACA")
                        )

                    else:
                        item.setBackground(
                            QColor("#374151")
                        )
                        item.setForeground(
                            QColor("#F3F4F6")
                        )

                self.table.setItem(
                    table_row,
                    column,
                    item,
                )

        # -----------------------------------------------------
        # Show a useful message below the table
        # -----------------------------------------------------

        if not rows:
            self.message_label.setText(
                "No saved ECG analyses yet. "
                "Analyze an ECG and save the result to see it here."
            )

        elif visible_count == 0:
            self.message_label.setText(
                "No records match your search. "
                "Try another name, report ID, filename or status."
            )

        else:
            self.message_label.setText(
                f"Showing {visible_count} of {len(rows)} saved record(s). "
                "NORMAL means no configured demo rule was triggered. "
                "FLAGGED means one or more configured rules were triggered."
            )

    # =========================================================
    # Global search support
    # =========================================================

    def set_search_text(self, text: str):

        self._search_text = text or ""

        # Keep the local search field in sync with the top bar.
        self.search_box.field.blockSignals(True)
        self.search_box.field.setText(self._search_text)
        self.search_box.field.blockSignals(False)

        self._fill_table()

    # =========================================================
    # Local search support
    # =========================================================

    def _filter_rows(self, text):

        self._search_text = text or ""
        self._fill_table()