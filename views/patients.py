"""
PulseMind - Patient Management
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from database.database import database_manager
from styles.theme import PALETTE, SPACING, Typography
from views.base_page import BasePage
from widgets.cards import InfoCard
from widgets.inputs import highlight_text


class PatientsPage(BasePage):

    page_key = "patients"
    page_title = "Patients"
    page_subtitle = "Manage patient records and history"

    def build(self):

        self._search_text = ""
        self._patients = []

        self._build_add_patient_card()
        self._build_patient_list()

        self.refresh()

        self.update_responsive_layout()

    # ==============================================================
    # Add patient
    # ==============================================================

    def _build_add_patient_card(self):

        card = InfoCard(
            "Add Patient",
            "Enter the patient's basic information.",
        )

        self.patient_form = QFormLayout()

        self.patient_form.setSpacing(
            SPACING.sm
        )

        # ----------------------------------------------------------
        # Name
        # ----------------------------------------------------------

        self.name_input = QLineEdit()

        self.name_input.setPlaceholderText(
            "Patient name"
        )

        self.name_input.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        # ----------------------------------------------------------
        # Age
        # ----------------------------------------------------------

        self.age_input = QLineEdit()

        self.age_input.setPlaceholderText(
            "Age"
        )

        self.age_input.setMinimumWidth(
            100
        )

        self.age_input.setMaximumWidth(
            180
        )

        self.age_input.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        # ----------------------------------------------------------
        # Gender
        # ----------------------------------------------------------

        self.gender_input = QComboBox()

        self.gender_input.addItems(
            [
                "Male",
                "Female",
                "Other",
            ]
        )

        self.gender_input.setMinimumWidth(
            100
        )

        self.gender_input.setMaximumWidth(
            180
        )

        self.gender_input.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        # ----------------------------------------------------------
        # Form
        # ----------------------------------------------------------

        self.patient_form.addRow(
            "Name",
            self.name_input,
        )

        self.patient_form.addRow(
            "Age",
            self.age_input,
        )

        self.patient_form.addRow(
            "Gender",
            self.gender_input,
        )

        card.body_layout().addLayout(
            self.patient_form
        )

        # ----------------------------------------------------------
        # Add button
        # ----------------------------------------------------------

        self.add_button = QPushButton(
            "Add Patient"
        )

        self.add_button.setMinimumHeight(
            40
        )

        self.add_button.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Fixed,
        )

        self.add_button.clicked.connect(
            self.add_patient
        )

        button_row = QHBoxLayout()

        button_row.setSpacing(
            SPACING.sm
        )

        button_row.addStretch(
            1
        )

        button_row.addWidget(
            self.add_button
        )

        card.body_layout().addLayout(
            button_row
        )

        self.content_layout.addWidget(
            card
        )

    # ==============================================================
    # Patient list
    # ==============================================================

    def _build_patient_list(self):

        self.patient_list_card = InfoCard(
            "Registered Patients",
            "Select a patient to start ECG analysis.",
        )

        self.patient_list_layout = (
            self.patient_list_card.body_layout()
        )

        self.content_layout.addWidget(
            self.patient_list_card
        )

    # ==============================================================
    # Refresh
    # ==============================================================

    def refresh(self):

        if not hasattr(
            self,
            "patient_list_layout",
        ):
            return

        while self.patient_list_layout.count():

            item = self.patient_list_layout.takeAt(
                0
            )

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

        try:

            patients = database_manager.get_patients()

        except Exception as error:

            label = QLabel(
                f"Could not load patients:\n{error}"
            )

            label.setWordWrap(
                True
            )

            self.patient_list_layout.addWidget(
                label
            )

            return

        self._patients = list(
            patients
        )

        if not self._patients:

            label = QLabel(
                "No patients registered yet."
            )

            label.setStyleSheet(
                f"""
                color: {PALETTE.text_secondary};
                """
            )

            self.patient_list_layout.addWidget(
                label
            )

            return

        self._display_patients()

    # ==============================================================
    # Display patients
    # ==============================================================

    def _display_patients(self):

        while self.patient_list_layout.count():

            item = self.patient_list_layout.takeAt(
                0
            )

            widget = item.widget()

            if widget is not None:

                widget.deleteLater()

        query = (
            self._search_text
            .strip()
            .lower()
        )

        visible_count = 0

        for patient in self._patients:

            name = str(
                patient["name"]
                or ""
            )

            patient_id = str(
                patient["patient_id"]
                or ""
            )

            searchable_text = (
                f"{name} {patient_id}"
            ).lower()

            if (
                query
                and query not in searchable_text
            ):
                continue

            self._add_patient_row(
                patient
            )

            visible_count += 1

        if visible_count == 0:

            label = QLabel(
                "No patients match your search."
            )

            label.setStyleSheet(
                f"""
                color: {PALETTE.text_secondary};
                """
            )

            self.patient_list_layout.addWidget(
                label
            )

        self.patient_list_layout.addStretch(
            1
        )

    # ==============================================================
    # Patient row
    # ==============================================================

    def _add_patient_row(
        self,
        patient,
    ):

        row = QWidget()

        row.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        layout = QHBoxLayout(
            row
        )

        layout.setContentsMargins(
            8,
            8,
            8,
            8,
        )

        layout.setSpacing(
            SPACING.md
        )

        # ----------------------------------------------------------
        # Name
        # ----------------------------------------------------------

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

        name.setWordWrap(
            True
        )

        name.setMinimumWidth(
            100
        )

        name.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred,
        )

        # ----------------------------------------------------------
        # Details
        # ----------------------------------------------------------

        details = QLabel(
            f"ID: {patient['patient_id']}    "
            f"Age: {patient['age']}    "
            f"Gender: {patient['gender']}"
        )

        details.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            """
        )

        details.setWordWrap(
            True
        )

        details.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        # ----------------------------------------------------------
        # Analysis button
        # ----------------------------------------------------------

        analyze_button = QPushButton(
            "Analysis"
        )

        analyze_button.setMinimumWidth(
            90
        )

        analyze_button.setMaximumWidth(
            150
        )

        analyze_button.setMinimumHeight(
            40
        )

        analyze_button.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Fixed,
        )

        analyze_button.clicked.connect(
            lambda checked=False,
            p=dict(patient):
            self.open_analysis(p)
        )

        layout.addWidget(
            name
        )

        layout.addWidget(
            details,
            stretch=1,
        )

        layout.addWidget(
            analyze_button
        )

        self.patient_list_layout.addWidget(
            row
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
            "_patients",
        ):

            self._display_patients()

    # ==============================================================
    # Add patient
    # ==============================================================

    def add_patient(self):

        name = (
            self.name_input
            .text()
            .strip()
        )

        age = (
            self.age_input
            .text()
            .strip()
        )

        gender = (
            self.gender_input
            .currentText()
            .strip()
        )

        try:

            patient = database_manager.add_patient(
                name,
                age,
                gender,
            )

        except ValueError as error:

            QMessageBox.warning(
                self,
                "Add Patient",
                str(error),
            )

            return

        except Exception as error:

            QMessageBox.critical(
                self,
                "Add Patient",
                str(error),
            )

            return

        self.name_input.clear()

        self.age_input.clear()

        self.gender_input.setCurrentIndex(
            0
        )

        self.refresh()

        message = QMessageBox(
            self
        )

        message.setWindowTitle(
            "Patient Added"
        )

        message.setText(
            "Patient added successfully."
        )

        message.setInformativeText(
            f"{patient['name']} is ready for ECG analysis."
        )

        analysis_button = message.addButton(
            "Start Analysis",
            QMessageBox.AcceptRole,
        )

        message.addButton(
            QMessageBox.Close
        )

        message.exec()

        if (
            message.clickedButton()
            == analysis_button
        ):

            self.open_analysis(
                dict(patient)
            )

    # ==============================================================
    # Open ECG analysis
    # ==============================================================

    def open_analysis(
        self,
        patient,
    ):

        main_window = self.window()

        if not hasattr(
            main_window,
            "_pages",
        ):
            return

        analysis_page = (
            main_window._pages.get(
                "analysis"
            )
        )

        if analysis_page is None:
            return

        analysis_page.set_patient(
            patient
        )

        main_window._nav_vm.set_active_page(
            "analysis"
        )

    # ==============================================================
    # Responsive layout
    # ==============================================================

    def update_responsive_layout(self):

        if not hasattr(
            self,
            "patient_form",
        ):
            return

        width = self.width()

        # ----------------------------------------------------------
        # Small screen
        # ----------------------------------------------------------

        if width < 650:

            self.patient_form.setRowWrapPolicy(
                QFormLayout.RowWrapPolicy.WrapLongRows
            )

            self.age_input.setMaximumWidth(
                100000
            )

            self.gender_input.setMaximumWidth(
                100000
            )

            self.age_input.setMinimumWidth(
                0
            )

            self.gender_input.setMinimumWidth(
                0
            )

            return

        # ----------------------------------------------------------
        # Normal screen
        # ----------------------------------------------------------

        self.patient_form.setRowWrapPolicy(
            QFormLayout.RowWrapPolicy.DontWrapRows
        )

        self.age_input.setMinimumWidth(
            100
        )

        self.age_input.setMaximumWidth(
            180
        )

        self.gender_input.setMinimumWidth(
            100
        )

        self.gender_input.setMaximumWidth(
            180
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