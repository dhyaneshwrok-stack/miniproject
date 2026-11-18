"""
PulseMind - Card Components
===========================

Reusable card components used throughout the application.
"""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from styles.theme import (
    PALETTE,
    RADIUS,
    SPACING,
    Typography,
)

from widgets.buttons import PrimaryButton


# =====================================================================
# Shadow
# =====================================================================

def _soft_shadow(
    widget: QWidget,
    blur: int = 28,
    y_offset: int = 10,
    alpha: int = 90,
) -> None:

    shadow = QGraphicsDropShadowEffect(widget)

    shadow.setBlurRadius(
        blur
    )

    shadow.setOffset(
        0,
        y_offset,
    )

    shadow.setColor(
        QColor(
            0,
            0,
            0,
            alpha,
        )
    )

    widget.setGraphicsEffect(
        shadow
    )


# =====================================================================
# Base Card
# =====================================================================

class _CardBase(QFrame):

    def __init__(
        self,
        parent=None,
    ) -> None:

        super().__init__(parent)

        self.setObjectName(
            "CardBase"
        )

        self.setStyleSheet(
            f"""
            QFrame#CardBase {{
                background-color: {PALETTE.bg_card};
                border: 1px solid {PALETTE.border};
                border-radius: {RADIUS.lg}px;
            }}

            QFrame#CardBase QLabel {{
                background-color: transparent;
            }}
            """
        )

        _soft_shadow(
            self
        )


# =====================================================================
# Stat Card
# =====================================================================

class StatCard(_CardBase):

    def __init__(
        self,
        title: str,
        value: str,
        icon: Optional[QIcon] = None,
        accent_color: str = PALETTE.accent,
        subtitle: str = "",
        parent=None,
    ) -> None:

        super().__init__(parent)

        self.setMinimumHeight(
            128
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            SPACING.lg,
            SPACING.md,
            SPACING.lg,
            SPACING.md,
        )

        layout.setSpacing(
            SPACING.xs
        )

        # -------------------------------------------------------------
        # Top row
        # -------------------------------------------------------------

        top_row = QHBoxLayout()

        top_row.setSpacing(
            SPACING.sm
        )

        # -------------------------------------------------------------
        # Title
        # -------------------------------------------------------------

        title_label = QLabel(
            title.upper()
        )

        title_label.setFont(
            Typography.caption()
        )

        title_label.setStyleSheet(
            f"""
            background-color: transparent;
            color: {PALETTE.text_secondary};
            letter-spacing: 1px;
            """
        )

        top_row.addWidget(
            title_label
        )

        top_row.addStretch(
            1
        )

        # -------------------------------------------------------------
        # Icon
        # -------------------------------------------------------------

        if icon is not None:

            icon_holder = QLabel()

            icon_holder.setPixmap(
                icon.pixmap(
                    20,
                    20,
                )
            )

            icon_holder.setStyleSheet(
                f"""
                background-color: rgba(229, 57, 53, 0.12);
                border-radius: {RADIUS.sm}px;
                padding: 6px;
                """
            )

            top_row.addWidget(
                icon_holder
            )

        layout.addLayout(
            top_row
        )

        # -------------------------------------------------------------
        # Value
        # -------------------------------------------------------------

        value_label = QLabel(
            value
        )

        value_label.setFont(
            Typography.display()
        )

        value_label.setStyleSheet(
            f"""
            background-color: transparent;
            color: {PALETTE.text_primary};
            """
        )

        layout.addWidget(
            value_label
        )

        # -------------------------------------------------------------
        # Subtitle
        # -------------------------------------------------------------

        if subtitle:

            subtitle_label = QLabel(
                subtitle
            )

            subtitle_label.setFont(
                Typography.body_small()
            )

            subtitle_label.setStyleSheet(
                f"""
                background-color: transparent;
                color: {accent_color};
                """
            )

            layout.addWidget(
                subtitle_label
            )

        layout.addStretch(
            1
        )


# =====================================================================
# Info Card
# =====================================================================

class InfoCard(_CardBase):

    def __init__(
        self,
        title: str = "",
        subtitle: str = "",
        parent=None,
    ) -> None:

        super().__init__(parent)

        self._layout = QVBoxLayout(
            self
        )

        self._layout.setContentsMargins(
            SPACING.lg,
            SPACING.lg,
            SPACING.lg,
            SPACING.lg,
        )

        self._layout.setSpacing(
            SPACING.xs
        )

        # -------------------------------------------------------------
        # Title
        # -------------------------------------------------------------

        if title:

            title_label = QLabel(
                title
            )

            title_label.setFont(
                Typography.h3()
            )

            title_label.setStyleSheet(
                f"""
                background-color: transparent;
                color: {PALETTE.text_primary};
                """
            )

            self._layout.addWidget(
                title_label
            )

        # -------------------------------------------------------------
        # Subtitle
        # -------------------------------------------------------------

        if subtitle:

            subtitle_label = QLabel(
                subtitle
            )

            subtitle_label.setFont(
                Typography.body_small()
            )

            subtitle_label.setWordWrap(
                True
            )

            subtitle_label.setStyleSheet(
                f"""
                background-color: transparent;
                color: {PALETTE.text_secondary};
                """
            )

            self._layout.addWidget(
                subtitle_label
            )

    def body_layout(
        self,
    ) -> QVBoxLayout:

        return self._layout


# =====================================================================
# Empty State Card
# =====================================================================

class EmptyStateCard(_CardBase):

    def __init__(
        self,
        icon: Optional[QIcon],
        title: str,
        description: str,
        action_text: str = "",
        parent=None,
    ) -> None:

        super().__init__(parent)

        self.setMinimumHeight(
            280
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            SPACING.xxl,
            SPACING.xxl,
            SPACING.xxl,
            SPACING.xxl,
        )

        layout.setSpacing(
            SPACING.sm
        )

        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # -------------------------------------------------------------
        # Icon
        # -------------------------------------------------------------

        if icon is not None:

            icon_frame = QFrame()

            icon_frame.setFixedSize(
                72,
                72,
            )

            icon_frame.setStyleSheet(
                f"""
                QFrame {{
                    background-color: {PALETTE.bg_secondary};
                    border: 1px solid {PALETTE.border};
                    border-radius: 36px;
                }}
                """
            )

            icon_layout = QVBoxLayout(
                icon_frame
            )

            icon_layout.setContentsMargins(
                0,
                0,
                0,
                0,
            )

            icon_label = QLabel()

            icon_label.setPixmap(
                icon.pixmap(
                    28,
                    28,
                )
            )

            icon_label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            icon_label.setStyleSheet(
                """
                background-color: transparent;
                """
            )

            icon_layout.addWidget(
                icon_label
            )

            layout.addWidget(
                icon_frame,
                alignment=Qt.AlignmentFlag.AlignHCenter,
            )

        # -------------------------------------------------------------
        # Title
        # -------------------------------------------------------------

        title_label = QLabel(
            title
        )

        title_label.setFont(
            Typography.h2()
        )

        title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title_label.setStyleSheet(
            f"""
            background-color: transparent;
            color: {PALETTE.text_primary};
            """
        )

        layout.addWidget(
            title_label
        )

        # -------------------------------------------------------------
        # Description
        # -------------------------------------------------------------

        desc_label = QLabel(
            description
        )

        desc_label.setFont(
            Typography.body()
        )

        desc_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        desc_label.setWordWrap(
            True
        )

        desc_label.setStyleSheet(
            f"""
            background-color: transparent;
            color: {PALETTE.text_secondary};
            """
        )

        desc_label.setMaximumWidth(
            420
        )

        layout.addWidget(
            desc_label,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )

        # -------------------------------------------------------------
        # Optional action
        # -------------------------------------------------------------

        if action_text:

            layout.addSpacing(
                SPACING.sm
            )

            action_button = PrimaryButton(
                action_text
            )

            action_button.setEnabled(
                False
            )

            action_button.setToolTip(
                "Available once this module is implemented"
            )

            layout.addWidget(
                action_button,
                alignment=Qt.AlignmentFlag.AlignHCenter,
            )