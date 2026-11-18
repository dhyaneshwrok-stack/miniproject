"""
PulseMind - Dialog Components
=============================

Responsive themed dialogs.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from styles.theme import PALETTE, RADIUS, SPACING, Typography
from widgets.buttons import (
    DangerButton,
    PrimaryButton,
    SecondaryButton,
)


class _DialogShell(QDialog):

    def __init__(
        self,
        parent=None,
        width: int = 420,
    ) -> None:

        super().__init__(
            parent
        )

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Dialog
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setModal(
            True
        )

        self._preferred_width = width

        self.setMinimumWidth(
            280
        )

        self.setMaximumWidth(
            width
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred,
        )

        outer = QVBoxLayout(
            self
        )

        outer.setContentsMargins(
            SPACING.sm,
            SPACING.sm,
            SPACING.sm,
            SPACING.sm,
        )

        self.card = QWidget()

        self.card.setObjectName(
            "DialogCard"
        )

        self.card.setStyleSheet(
            f"""
            #DialogCard {{
                background-color: {PALETTE.bg_card};
                border: 1px solid {PALETTE.border};
                border-radius: {RADIUS.xl}px;
            }}
            """
        )

        shadow = QGraphicsDropShadowEffect(
            self.card
        )

        shadow.setBlurRadius(
            48
        )

        shadow.setOffset(
            0,
            16
        )

        shadow.setColor(
            QColor(
                0,
                0,
                0,
                140,
            )
        )

        self.card.setGraphicsEffect(
            shadow
        )

        outer.addWidget(
            self.card
        )

        self.card_layout = QVBoxLayout(
            self.card
        )

        self.card_layout.setContentsMargins(
            SPACING.lg,
            SPACING.lg,
            SPACING.lg,
            SPACING.lg,
        )

        self.card_layout.setSpacing(
            SPACING.md
        )

    def showEvent(
        self,
        event,
    ):

        super().showEvent(
            event
        )

        parent = self.parentWidget()

        if parent is not None:

            available_width = (
                parent.width()
            )

            target_width = min(
                self._preferred_width,
                max(
                    280,
                    available_width - 32,
                ),
            )

            self.resize(
                target_width,
                self.sizeHint().height(),
            )


class ConfirmationDialog(
    _DialogShell
):

    def __init__(
        self,
        title: str,
        message: str,
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel",
        danger: bool = False,
        parent=None,
    ):

        super().__init__(
            parent
        )

        self.confirmed = False

        title_label = QLabel(
            title
        )

        title_label.setFont(
            Typography.h2()
        )

        title_label.setStyleSheet(
            f"""
            color: {PALETTE.text_primary};
            """
        )

        title_label.setWordWrap(
            True
        )

        self.card_layout.addWidget(
            title_label
        )

        message_label = QLabel(
            message
        )

        message_label.setFont(
            Typography.body()
        )

        message_label.setWordWrap(
            True
        )

        message_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            """
        )

        self.card_layout.addWidget(
            message_label
        )

        self.card_layout.addSpacing(
            SPACING.sm
        )

        button_row = QHBoxLayout()

        button_row.setSpacing(
            SPACING.sm
        )

        button_row.addStretch(
            1
        )

        cancel_btn = SecondaryButton(
            cancel_text
        )

        cancel_btn.clicked.connect(
            self.reject
        )

        button_row.addWidget(
            cancel_btn
        )

        if danger:

            confirm_btn = DangerButton(
                confirm_text
            )

        else:

            confirm_btn = PrimaryButton(
                confirm_text
            )

        confirm_btn.clicked.connect(
            self._on_confirm
        )

        button_row.addWidget(
            confirm_btn
        )

        self.card_layout.addLayout(
            button_row
        )

    def _on_confirm(
        self,
    ):

        self.confirmed = True

        self.accept()


class MessageDialog(
    _DialogShell
):

    def __init__(
        self,
        title: str,
        message: str,
        ok_text: str = "OK",
        parent=None,
    ):

        super().__init__(
            parent
        )

        title_label = QLabel(
            title
        )

        title_label.setFont(
            Typography.h2()
        )

        title_label.setStyleSheet(
            f"""
            color: {PALETTE.text_primary};
            """
        )

        title_label.setWordWrap(
            True
        )

        self.card_layout.addWidget(
            title_label
        )

        message_label = QLabel(
            message
        )

        message_label.setFont(
            Typography.body()
        )

        message_label.setWordWrap(
            True
        )

        message_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            """
        )

        self.card_layout.addWidget(
            message_label
        )

        self.card_layout.addSpacing(
            SPACING.sm
        )

        button_row = QHBoxLayout()

        button_row.addStretch(
            1
        )

        ok_btn = PrimaryButton(
            ok_text
        )

        ok_btn.clicked.connect(
            self.accept
        )

        button_row.addWidget(
            ok_btn
        )

        self.card_layout.addLayout(
            button_row
        )


class LoadingDialog(
    _DialogShell
):

    def __init__(
        self,
        message: str = "Loading...",
        parent=None,
    ):

        super().__init__(
            parent,
            width=320,
        )

        self.setWindowModality(
            Qt.WindowModality.ApplicationModal
        )

        label = QLabel(
            message
        )

        label.setFont(
            Typography.body_medium()
        )

        label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        label.setWordWrap(
            True
        )

        label.setStyleSheet(
            f"""
            color: {PALETTE.text_primary};
            """
        )

        self.card_layout.addWidget(
            label
        )

        progress = QProgressBar()

        progress.setRange(
            0,
            0,
        )

        progress.setTextVisible(
            False
        )

        progress.setFixedHeight(
            6
        )

        progress.setStyleSheet(
            f"""
            QProgressBar {{
                background-color: {PALETTE.bg_secondary};
                border-radius: 3px;
            }}

            QProgressBar::chunk {{
                background-color: {PALETTE.accent};
                border-radius: 3px;
            }}
            """
        )

        self.card_layout.addWidget(
            progress
        )