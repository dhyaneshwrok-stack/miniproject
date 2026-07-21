"""
PulseMind - ECG Analysis Page
================================

Phase 1 placeholder for PRD Modules 4-7 (Dataset Loader, Waveform
Viewer, Signal Processing, Parameter Calculation). Only the layout
skeleton exists; no dataset parsing or signal processing runs yet.
"""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from styles.theme import PALETTE, SPACING, Typography
from utils.icons import icon
from views.base_page import BasePage
from widgets.buttons import SecondaryButton
from widgets.cards import EmptyStateCard, InfoCard


class AnalysisPage(BasePage):
    page_key = "analysis"
    page_title = "ECG Analysis"
    page_subtitle = "Load, visualize, and process ECG signals"

    def build(self) -> None:
        columns = QHBoxLayout()
        columns.setSpacing(SPACING.lg)
        columns.addWidget(self._build_viewer_placeholder(), stretch=2)
        columns.addWidget(self._build_parameters_placeholder(), stretch=1)
        self.content_layout.addLayout(columns)

    def _build_viewer_placeholder(self) -> QWidget:
        wrapper = QVBoxLayout()
        card = InfoCard("ECG Dataset & Waveform Viewer",
                         "Load a CSV or TXT dataset to preview the waveform here")
        row = QHBoxLayout()
        row.setSpacing(SPACING.sm)
        browse_btn = SecondaryButton("Browse File", icon("search", color=PALETTE.text_secondary, size=15))
        browse_btn.setEnabled(False)
        browse_btn.setToolTip("Dataset loading arrives in Phase 3")
        row.addWidget(browse_btn)
        row.addStretch(1)
        card.body_layout().addLayout(row)
        card.body_layout().addWidget(
            EmptyStateCard(
                icon=icon("analysis", color=PALETTE.text_secondary, size=26),
                title="No Signal Loaded",
                description="Once a dataset is loaded, an interactive waveform with zoom, pan, and grid view will render here.",
            )
        )

        container = QWidget()
        container.setLayout(card.body_layout())
        return card

    def _build_parameters_placeholder(self) -> QWidget:
        card = InfoCard("ECG Parameters", "Calculated once a signal is loaded")
        for label in ("Heart Rate (BPM)", "RR Interval", "Average RR",
                      "Signal Duration", "Number of Beats"):
            row = QHBoxLayout()
            key = _label(label, PALETTE.text_secondary)
            value = _label("—", PALETTE.text_primary, bold=True)
            row.addWidget(key)
            row.addStretch(1)
            row.addWidget(value)
            card.body_layout().addLayout(row)
        return card


def _label(text: str, color: str, bold: bool = False):
    from PySide6.QtWidgets import QLabel
    lbl = QLabel(text)
    lbl.setFont(Typography.body_medium() if bold else Typography.body_small())
    lbl.setStyleSheet(f"color: {color};")
    return lbl
