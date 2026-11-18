from pathlib import Path

import numpy as np

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from database.database import database_manager
from services.ecg_service import analyze_file
from services.report_generator import generate_pdf_report

from styles.theme import PALETTE, SPACING, Typography
from utils.icons import icon

from views.base_page import BasePage

from widgets.buttons import SecondaryButton
from widgets.cards import InfoCard


# ==============================================================
# ECG Canvas
# ==============================================================

class ECGCanvas(FigureCanvas):

    def __init__(
        self,
        parent=None,
    ):

        self.figure = Figure(
            figsize=(8, 4),
            dpi=100,
        )

        self.axes = self.figure.add_subplot(
            111
        )

        super().__init__(
            self.figure
        )

        self.setParent(
            parent
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

    # ----------------------------------------------------------
    # Show ECG signal
    # ----------------------------------------------------------

    def show_signal(
        self,
        time,
        raw,
        filtered,
        r_peaks,
    ):

        self.axes.clear()

        self.axes.plot(
            time,
            raw,
            linewidth=0.6,
            alpha=0.35,
            label="Raw ECG",
        )

        self.axes.plot(
            time,
            filtered,
            linewidth=0.8,
            label="Filtered ECG",
        )

        if len(r_peaks):

            self.axes.scatter(
                time[r_peaks],
                filtered[r_peaks],
                s=18,
                label="R-peaks",
                zorder=5,
            )

        self.axes.set_xlabel(
            "Time (s)"
        )

        self.axes.set_ylabel(
            "Amplitude"
        )

        self.axes.grid(
            True,
            alpha=0.2,
        )

        self.axes.legend(
            loc="upper right"
        )

        self.figure.tight_layout()

        self.draw()

    # ----------------------------------------------------------
    # Clear plot
    # ----------------------------------------------------------

    def clear_plot(
        self,
    ):

        self.axes.clear()

        self.axes.set_title(
            "No ECG signal loaded"
        )

        self.axes.grid(
            True,
            alpha=0.2,
        )

        self.figure.tight_layout()

        self.draw()


# ==============================================================
# Analysis Page
# ==============================================================

class AnalysisPage(BasePage):

    page_key = "analysis"

    page_title = "ECG Analysis"

    page_subtitle = (
        "Load, process, and analyze ECG signals"
    )

    # ==========================================================
    # Build
    # ==========================================================

    def build(self):

        self.result = None

        self.report_path = None

        self.selected_patient = None

        # ------------------------------------------------------
        # Top controls
        # ------------------------------------------------------

        self.top_controls = QHBoxLayout()

        self.top_controls.setSpacing(
            SPACING.sm
        )

        # ------------------------------------------------------
        # Patient ID
        # ------------------------------------------------------

        self.patient_id = QLineEdit()

        self.patient_id.setPlaceholderText(
            "Patient ID"
        )

        self.patient_id.setMinimumWidth(
            120
        )

        self.patient_id.setMaximumWidth(
            180
        )

        self.patient_id.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.patient_id.setReadOnly(
            True
        )

        # ------------------------------------------------------
        # Patient name
        # ------------------------------------------------------

        self.patient_name = QLineEdit()

        self.patient_name.setPlaceholderText(
            "Patient name"
        )

        self.patient_name.setMinimumWidth(
            140
        )

        self.patient_name.setMaximumWidth(
            220
        )

        self.patient_name.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.patient_name.setReadOnly(
            True
        )

        # ------------------------------------------------------
        # File label
        # ------------------------------------------------------

        self.file_label = QLabel(
            "No ECG file selected"
        )

        self.file_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            """
        )

        self.file_label.setWordWrap(
            True
        )

        self.file_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        # ------------------------------------------------------
        # Browse button
        # ------------------------------------------------------

        self.browse_button = SecondaryButton(
            "Load ECG File",
            icon(
                "search",
                color=PALETTE.text_secondary,
                size=15,
            ),
        )

        self.browse_button.clicked.connect(
            self.load_ecg
        )

        # ------------------------------------------------------
        # Save button
        # ------------------------------------------------------

        self.save_button = SecondaryButton(
            "Save Analysis"
        )

        self.save_button.setEnabled(
            False
        )

        self.save_button.clicked.connect(
            self.save_analysis
        )

        # ------------------------------------------------------
        # PDF button
        # ------------------------------------------------------

        self.pdf_button = SecondaryButton(
            "Export PDF"
        )

        self.pdf_button.setEnabled(
            False
        )

        self.pdf_button.clicked.connect(
            self.export_pdf
        )

        # ------------------------------------------------------
        # Add controls
        # ------------------------------------------------------

        self.top_controls.addWidget(
            self.patient_id
        )

        self.top_controls.addWidget(
            self.patient_name
        )

        self.top_controls.addWidget(
            self.file_label,
            stretch=1,
        )

        self.top_controls.addWidget(
            self.browse_button
        )

        self.top_controls.addWidget(
            self.save_button
        )

        self.top_controls.addWidget(
            self.pdf_button
        )

        self.content_layout.addLayout(
            self.top_controls
        )

        # ------------------------------------------------------
        # Main analysis columns
        # ------------------------------------------------------

        self.analysis_columns = QHBoxLayout()

        self.analysis_columns.setSpacing(
            SPACING.lg
        )

        # ------------------------------------------------------
        # ECG waveform card
        # ------------------------------------------------------

        self.viewer_card = InfoCard(
            "ECG Waveform",
            "Raw signal, filtered signal, and detected R-peaks",
        )

        self.canvas = ECGCanvas()

        self.canvas.setMinimumHeight(
            420
        )

        self.viewer_card.body_layout().addWidget(
            self.canvas
        )

        self.analysis_columns.addWidget(
            self.viewer_card,
            stretch=2,
        )

        # ------------------------------------------------------
        # Parameters
        # ------------------------------------------------------

        self.parameter_card = (
            self._build_parameter_card()
        )

        self.analysis_columns.addWidget(
            self.parameter_card,
            stretch=1,
        )

        self.content_layout.addLayout(
            self.analysis_columns
        )

        # ------------------------------------------------------
        # Status
        # ------------------------------------------------------

        self.status_label = QLabel(
            "Select a patient first, then load an ECG file."
        )

        self.status_label.setWordWrap(
            True
        )

        self.status_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            padding: 8px;
            """
        )

        self.content_layout.addWidget(
            self.status_label
        )

        # ------------------------------------------------------
        # Initial plot
        # ------------------------------------------------------

        self.canvas.clear_plot()

        self.update_responsive_layout()

    # ==============================================================
    # Responsive layout
    # ==============================================================

    def update_responsive_layout(
        self,
    ):

        width = self.width()

        # ------------------------------------------------------
        # Very small window
        # ------------------------------------------------------

        if width < 650:

            self.analysis_columns.setDirection(
                QVBoxLayout.Direction.TopToBottom
            )

            self.canvas.setMinimumHeight(
                320
            )

            self.top_controls.setDirection(
                QVBoxLayout.Direction.TopToBottom
            )

            self.patient_id.setMaximumWidth(
                100000
            )

            self.patient_name.setMaximumWidth(
                100000
            )

            self.patient_id.setMinimumWidth(
                0
            )

            self.patient_name.setMinimumWidth(
                0
            )

            self.browse_button.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
            )

            self.save_button.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
            )

            self.pdf_button.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Fixed,
            )

            return

        # ------------------------------------------------------
        # Medium window
        # ------------------------------------------------------

        if width < 900:

            self.analysis_columns.setDirection(
                QVBoxLayout.Direction.TopToBottom
            )

            self.canvas.setMinimumHeight(
                360
            )

            self.top_controls.setDirection(
                QVBoxLayout.Direction.LeftToRight
            )

            self.patient_id.setMinimumWidth(
                100
            )

            self.patient_id.setMaximumWidth(
                150
            )

            self.patient_name.setMinimumWidth(
                120
            )

            self.patient_name.setMaximumWidth(
                180
            )

            return

        # ------------------------------------------------------
        # Normal desktop
        # ------------------------------------------------------

        self.analysis_columns.setDirection(
            QVBoxLayout.Direction.LeftToRight
        )

        self.canvas.setMinimumHeight(
            420
        )

        self.top_controls.setDirection(
            QVBoxLayout.Direction.LeftToRight
        )

        self.patient_id.setMinimumWidth(
            120
        )

        self.patient_id.setMaximumWidth(
            180
        )

        self.patient_name.setMinimumWidth(
            140
        )

        self.patient_name.setMaximumWidth(
            220
        )

    # ==============================================================
    # Resize event
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
    # Patient selection
    # ==============================================================

    def set_patient(
        self,
        patient,
    ):

        self.selected_patient = dict(
            patient
        )

        self.patient_id.setText(
            str(
                patient["patient_id"]
            )
        )

        self.patient_name.setText(
            str(
                patient["name"]
            )
        )

        self.result = None

        self.report_path = None

        self.file_label.setText(
            "No ECG file selected"
        )

        self.save_button.setEnabled(
            False
        )

        self.pdf_button.setEnabled(
            False
        )

        self.findings_label.setText(
            "No analysis yet."
        )

        self.status_label.setText(
            f"Patient selected: "
            f"{patient['name']} "
            f"(Age {patient['age']}, "
            f"{patient['gender']}). "
            "Load an ECG file to start analysis."
        )

        self.canvas.clear_plot()

    # ==============================================================
    # Parameter card
    # ==============================================================

    def _build_parameter_card(
        self,
    ):

        card = InfoCard(
            "ECG Parameters",
            "Values calculated from the loaded signal",
        )

        self.values = {}

        fields = [
            (
                "Heart Rate",
                "heart_rate",
                "BPM",
            ),
            (
                "Average RR",
                "average_rr",
                "s",
            ),
            (
                "PR Interval",
                "pr_ms",
                "ms",
            ),
            (
                "QRS Duration",
                "qrs_ms",
                "ms",
            ),
            (
                "QT Interval",
                "qt_ms",
                "ms",
            ),
            (
                "QTc",
                "qtc_ms",
                "ms",
            ),
            (
                "Detected Beats",
                "beat_count",
                "",
            ),
            (
                "Status",
                "status",
                "",
            ),
        ]

        for label, key, unit in fields:

            row = QHBoxLayout()

            key_label = QLabel(
                label
            )

            key_label.setFont(
                Typography.body_small()
            )

            key_label.setStyleSheet(
                f"""
                color: {PALETTE.text_secondary};
                """
            )

            key_label.setWordWrap(
                True
            )

            value_label = QLabel(
                "—"
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

            self.values[key] = (
                value_label,
                unit,
            )

            row.addWidget(
                key_label,
                stretch=1,
            )

            row.addStretch(
                1
            )

            row.addWidget(
                value_label
            )

            card.body_layout().addLayout(
                row
            )

        # ------------------------------------------------------
        # Findings
        # ------------------------------------------------------

        self.findings_label = QLabel(
            "No analysis yet."
        )

        self.findings_label.setWordWrap(
            True
        )

        self.findings_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            padding-top: 10px;
            """
        )

        card.body_layout().addWidget(
            self.findings_label
        )

        return card

    # ==============================================================
    # Load ECG
    # ==============================================================

    def load_ecg(
        self,
    ):

        if self.selected_patient is None:

            QMessageBox.information(
                self,
                "Select Patient",
                "Please add/select a patient before starting ECG analysis.",
            )

            return

        file_path, _ = (
            QFileDialog.getOpenFileName(
                self,
                "Select ECG File",
                "",
                "ECG Files (*.csv *.txt);;"
                "CSV Files (*.csv);;"
                "Text Files (*.txt)",
            )
        )

        if not file_path:
            return

        try:

            self.status_label.setText(
                "Processing ECG signal..."
            )

            self.status_label.repaint()

            self.result = analyze_file(
                file_path
            )

            self._display_result()

        except ValueError as error:

            if (
                "sampling rate"
                in str(error).lower()
            ):

                self._load_with_manual_sampling_rate(
                    file_path
                )

            else:

                QMessageBox.warning(
                    self,
                    "ECG Analysis",
                    str(error),
                )

                self.status_label.setText(
                    "ECG analysis failed."
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "ECG Analysis",
                str(error),
            )

            self.status_label.setText(
                "ECG analysis failed."
            )

    # ==============================================================
    # Manual sampling rate
    # ==============================================================

    def _load_with_manual_sampling_rate(
        self,
        file_path,
    ):

        from PySide6.QtWidgets import (
            QInputDialog,
        )

        rate, accepted = (
            QInputDialog.getDouble(
                self,
                "Sampling Rate",
                "Enter ECG sampling rate in Hz:",
                360.0,
                1.0,
                5000.0,
                2,
            )
        )

        if not accepted:

            self.status_label.setText(
                "Sampling rate was not provided."
            )

            return

        try:

            self.result = analyze_file(
                file_path,
                sample_rate=rate,
            )

            self._display_result()

        except Exception as error:

            QMessageBox.warning(
                self,
                "ECG Analysis",
                str(error),
            )

            self.status_label.setText(
                "ECG analysis failed."
            )

    # ==============================================================
    # Display result
    # ==============================================================

    def _display_result(
        self,
    ):

        result = self.result

        # ------------------------------------------------------
        # File name and ECG waveform
        # ------------------------------------------------------

        self.file_label.setText(
            str(result.get("file_name", "ECG file loaded"))
        )

        self.canvas.show_signal(
            result["time"],
            result["raw_signal"],
            result["filtered_signal"],
            result["r_peaks"],
        )

        # ------------------------------------------------------
        # Display calculated parameters
        # ------------------------------------------------------

        for key, (label, unit) in self.values.items():

            value = result.get(key)

            if value is None:
                text = "Not estimated"

            elif isinstance(value, (float, np.floating)):
                text = f"{float(value):.2f}"

            else:
                text = str(value)

            if unit and text != "Not estimated":
                text += f" {unit}"

            label.setText(text)

        # ------------------------------------------------------
        # Clear NORMAL / FLAGGED result message
        # ------------------------------------------------------

        status = str(result.get("status", "UNKNOWN")).upper()

        if status == "NORMAL":
            status_heading = "NORMAL"
            status_message = (
                "No issues were flagged by the configured demo rules."
            )
            status_color = "#22C55E"

        elif status == "FLAGGED":
            status_heading = "FLAGGED"
            status_message = (
                "One or more configured demo rules flagged this ECG. "
                "Review the findings and measurements."
            )
            status_color = "#F87171"

        else:
            status_heading = "UNKNOWN"
            status_message = (
                "The analysis did not return a recognized status."
            )
            status_color = PALETTE.text_secondary

        self.status_label.setText(
            f"{status_heading}\n{status_message}"
        )
        self.status_label.setStyleSheet(
            f"color: {status_color}; padding: 10px; font-weight: bold;"
        )

        # ------------------------------------------------------
        # Findings and academic-use note
        # ------------------------------------------------------

        findings = result.get("findings", [])

        if findings:
            findings_text = "\n".join(
                f"• {item}" for item in findings
            )
        else:
            findings_text = "No additional findings were returned."

        notes = result.get("notes", "")
        if notes:
            findings_text += f"\n\n{notes}"

        self.findings_label.setText(findings_text)

        # ------------------------------------------------------
        # Enable save and PDF export
        # ------------------------------------------------------

        self.save_button.setEnabled(True)
        self.pdf_button.setEnabled(True)

    # ==============================================================
    # Save analysis
    # ==============================================================

    def save_analysis(
        self,
    ):

        if not self.result:
            return

        if not self.selected_patient:

            QMessageBox.warning(
                self,
                "Save Analysis",
                "No patient is selected.",
            )

            return

        try:

            report_id = (
                database_manager.save_result(
                    self.result,
                    patient_name=(
                        self.selected_patient[
                            "name"
                        ]
                    ),
                    patient_code=(
                        self.selected_patient[
                            "patient_id"
                        ]
                    ),
                )
            )

            self.status_label.setText(
                f"Analysis saved successfully. "
                f"Report ID: {report_id}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Save Analysis",
                str(error),
            )

    # ==============================================================
    # Export PDF
    # ==============================================================

    def export_pdf(
        self,
    ):

        if not self.result:
            return

        if not self.selected_patient:

            QMessageBox.warning(
                self,
                "PDF Report",
                "No patient is selected.",
            )

            return

        default_name = (
            Path(
                self.result[
                    "file_name"
                ]
            ).stem
            + "_report.pdf"
        )

        output_path, _ = (
            QFileDialog.getSaveFileName(
                self,
                "Save ECG Report",
                default_name,
                "PDF Files (*.pdf)",
            )
        )

        if not output_path:
            return

        try:

            generate_pdf_report(
                output_path,
                self.selected_patient[
                    "name"
                ],
                self.selected_patient[
                    "patient_id"
                ],
                self.result,
            )

            self.report_path = (
                output_path
            )

            self.status_label.setText(
                f"PDF report created: "
                f"{Path(output_path).name}"
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "PDF Report",
                str(error),
            )