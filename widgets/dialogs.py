"""
PulseMind - Dialog Components
================================

Frameless, themed dialogs: confirmation prompts, simple message boxes,
and an indeterminate loading overlay. All share a common rounded-card
shell rather than the OS's native dialog chrome, per the mood board's
"everything should feel custom designed" requirement.
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QPropertyAnimation, QRect, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog, QGraphicsDropShadowEffect, QHBoxLayout, QLabel, QProgressBar,
    QVBoxLayout, QWidget,
)

from styles.theme import PALETTE, RADIUS, SPACING, Typography
from widgets.buttons import DangerButton, PrimaryButton, SecondaryButton


class _DialogShell(QDialog):
    """Frameless, centered, drop-shadowed dialog base."""

    def __init__(self, parent=None, width: int = 420) -> None:
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedWidth(width)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 20, 20, 20)

        self.card = QWidget()
        self.card.setObjectName("DialogCard")
        self.card.setStyleSheet(f"""
            #DialogCard {{
                background-color: {PALETTE.bg_card};
                border: 1px solid {PALETTE.border};
                border-radius: {RADIUS.xl}px;
            }}
        """)
        shadow = QGraphicsDropShadowEffect(self.card)
        shadow.setBlurRadius(48)
        shadow.setOffset(0, 16)
        shadow.setColor(QColor(0, 0, 0, 140))
        self.card.setGraphicsEffect(shadow)
        outer.addWidget(self.card)

        self.card_layout = QVBoxLayout(self.card)
        self.card_layout.setContentsMargins(SPACING.xl, SPACING.xl, SPACING.xl, SPACING.xl)
        self.card_layout.setSpacing(SPACING.md)


class ConfirmationDialog(_DialogShell):
    """Yes/No style confirmation with a configurable danger tone."""

    def __init__(self, title: str, message: str, confirm_text: str = "Confirm",
                 cancel_text: str = "Cancel", danger: bool = False, parent=None):
        super().__init__(parent)
        self.confirmed: bool = False

        title_label = QLabel(title)
        title_label.setFont(Typography.h2())
        title_label.setStyleSheet(f"color: {PALETTE.text_primary};")
        self.card_layout.addWidget(title_label)

        message_label = QLabel(message)
        message_label.setFont(Typography.body())
        message_label.setWordWrap(True)
        message_label.setStyleSheet(f"color: {PALETTE.text_secondary};")
        self.card_layout.addWidget(message_label)

        self.card_layout.addSpacing(SPACING.sm)

        button_row = QHBoxLayout()
        button_row.setSpacing(SPACING.sm)
        button_row.addStretch(1)

        cancel_btn = SecondaryButton(cancel_text)
        cancel_btn.clicked.connect(self.reject)
        button_row.addWidget(cancel_btn)

        confirm_btn = DangerButton(confirm_text) if danger else PrimaryButton(confirm_text)
        confirm_btn.clicked.connect(self._on_confirm)
        button_row.addWidget(confirm_btn)

        self.card_layout.addLayout(button_row)

    def _on_confirm(self) -> None:
        self.confirmed = True
        self.accept()


class MessageDialog(_DialogShell):
    """Simple informational / success / error message dialog."""

    def __init__(self, title: str, message: str, ok_text: str = "OK", parent=None):
        super().__init__(parent)

        title_label = QLabel(title)
        title_label.setFont(Typography.h2())
        title_label.setStyleSheet(f"color: {PALETTE.text_primary};")
        self.card_layout.addWidget(title_label)

        message_label = QLabel(message)
        message_label.setFont(Typography.body())
        message_label.setWordWrap(True)
        message_label.setStyleSheet(f"color: {PALETTE.text_secondary};")
        self.card_layout.addWidget(message_label)

        self.card_layout.addSpacing(SPACING.sm)

        button_row = QHBoxLayout()
        button_row.addStretch(1)
        ok_btn = PrimaryButton(ok_text)
        ok_btn.clicked.connect(self.accept)
        button_row.addWidget(ok_btn)
        self.card_layout.addLayout(button_row)


class LoadingDialog(_DialogShell):
    """Indeterminate loading overlay for future async operations."""

    def __init__(self, message: str = "Loading...", parent=None):
        super().__init__(parent, width=320)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        label = QLabel(message)
        label.setFont(Typography.body_medium())
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"color: {PALETTE.text_primary};")
        self.card_layout.addWidget(label)

        progress = QProgressBar()
        progress.setRange(0, 0)  # indeterminate
        progress.setTextVisible(False)
        progress.setFixedHeight(6)
        progress.setStyleSheet(f"""
            QProgressBar {{
                background-color: {PALETTE.bg_secondary};
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background-color: {PALETTE.accent};
                border-radius: 3px;
            }}
        """)
        self.card_layout.addWidget(progress)
