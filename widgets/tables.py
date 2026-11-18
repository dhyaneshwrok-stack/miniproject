"""
PulseMind - Styled Table Widget
================================

Responsive table used by History and other data pages.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
)

from styles.theme import PALETTE, RADIUS, Typography


class StyledTableWidget(
    QTableWidget
):

    def __init__(
        self,
        headers: list[str] | None = None,
        parent=None,
    ) -> None:

        super().__init__(
            parent
        )

        self.setObjectName(
            "StyledTable"
        )

        # ----------------------------------------------------------
        # Editing
        # ----------------------------------------------------------

        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.setAlternatingRowColors(
            False
        )

        self.setShowGrid(
            False
        )

        self.verticalHeader().setVisible(
            False
        )

        self.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

        self.setFont(
            Typography.body_small()
        )

        # ----------------------------------------------------------
        # Responsive scrolling
        # ----------------------------------------------------------

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # ----------------------------------------------------------
        # Headers
        # ----------------------------------------------------------

        if headers:

            self.setColumnCount(
                len(headers)
            )

            self.setHorizontalHeaderLabels(
                headers
            )

        header = self.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        header.setHighlightSections(
            False
        )

        header.setFont(
            Typography.caption()
        )

        # ----------------------------------------------------------
        # Styling
        # ----------------------------------------------------------

        self.setStyleSheet(
            f"""
            QTableWidget#StyledTable {{
                background-color: {PALETTE.bg_card};
                border: 1px solid {PALETTE.border};
                border-radius: {RADIUS.lg}px;
                gridline-color: {PALETTE.border};
                color: {PALETTE.text_primary};
            }}

            QTableWidget#StyledTable::item {{
                padding: 10px;
                border-bottom: 1px solid {PALETTE.border};
            }}

            QTableWidget#StyledTable::item:selected {{
                background-color: rgba(
                    229,
                    57,
                    53,
                    0.14
                );

                color: {PALETTE.text_primary};
            }}

            QHeaderView::section {{
                background-color: {PALETTE.bg_secondary};
                color: {PALETTE.text_secondary};
                padding: 12px 10px;
                border: none;
                border-bottom: 1px solid {PALETTE.border};
                text-transform: uppercase;
            }}
            """
        )

        self.setRowCount(
            0
        )