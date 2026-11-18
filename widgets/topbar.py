"""
PulseMind - Top Bar
===================

Responsive top navigation strip.
"""

from __future__ import annotations

from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
)

from styles.theme import PALETTE, RADIUS, SPACING, Typography
from utils.icons import icon
from widgets.buttons import IconButton
from widgets.inputs import SearchBox


class TopBar(QFrame):
    """Responsive top bar shown above every page."""

    search_changed = Signal(str)

    def __init__(
        self,
        parent=None,
    ) -> None:

        super().__init__(
            parent
        )

        self.setObjectName(
            "TopBar"
        )

        self.setMinimumHeight(
            68
        )

        self.setMaximumHeight(
            90
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.setStyleSheet(
            f"""
            #TopBar {{
                background-color: {PALETTE.bg_primary};
                border-bottom: 1px solid {PALETTE.border};
            }}
            """
        )

        self.layout_main = QHBoxLayout(
            self
        )

        self.layout_main.setContentsMargins(
            SPACING.lg,
            SPACING.sm,
            SPACING.lg,
            SPACING.sm,
        )

        self.layout_main.setSpacing(
            SPACING.sm
        )

        # ----------------------------------------------------------
        # Title
        # ----------------------------------------------------------

        self.title_box = QVBoxLayout()

        self.title_box.setSpacing(
            0
        )

        self.title_label = QLabel(
            "Dashboard"
        )

        self.title_label.setFont(
            Typography.h1()
        )

        self.title_label.setStyleSheet(
            f"""
            color: {PALETTE.text_primary};
            """
        )

        self.subtitle_label = QLabel(
            "Welcome back"
        )

        self.subtitle_label.setFont(
            Typography.body_small()
        )

        self.subtitle_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            """
        )

        self.subtitle_label.setWordWrap(
            True
        )

        self.title_box.addWidget(
            self.title_label
        )

        self.title_box.addWidget(
            self.subtitle_label
        )

        self.layout_main.addLayout(
            self.title_box,
            stretch=1,
        )

        # ----------------------------------------------------------
        # Search
        # ----------------------------------------------------------

        self.search_box = SearchBox(
            "Search patient names..."
        )

        self.search_box.setMinimumWidth(
            160
        )

        self.search_box.setMaximumWidth(
            280
        )

        self.search_box.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.search_box.field.textChanged.connect(
            self.search_changed.emit
        )

        self.layout_main.addWidget(
            self.search_box
        )

        # ----------------------------------------------------------
        # Date
        # ----------------------------------------------------------

        self.date_label = QLabel(
            QDate.currentDate().toString(
                "ddd, MMM d, yyyy"
            )
        )

        self.date_label.setFont(
            Typography.body_small()
        )

        self.date_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.date_label.setStyleSheet(
            f"""
            color: {PALETTE.text_secondary};
            background-color: {PALETTE.bg_secondary};
            border: 1px solid {PALETTE.border};
            border-radius: {RADIUS.pill}px;
            padding: 8px 12px;
            """
        )

        self.layout_main.addWidget(
            self.date_label
        )

        # ----------------------------------------------------------
        # Notification
        # ----------------------------------------------------------

        self.notif_btn = IconButton(
            icon(
                "bell",
                color=PALETTE.text_secondary,
                size=18,
            ),
            size=40,
        )

        self.layout_main.addWidget(
            self.notif_btn
        )

        # ----------------------------------------------------------
        # Avatar
        # ----------------------------------------------------------

        self.avatar = QLabel(
            "PM"
        )

        self.avatar.setFixedSize(
            40,
            40,
        )

        self.avatar.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.avatar.setFont(
            Typography.body_medium()
        )

        self.avatar.setStyleSheet(
            f"""
            background-color: {PALETTE.accent};
            color: {PALETTE.text_on_accent};
            border-radius: 20px;
            """
        )

        self.layout_main.addWidget(
            self.avatar
        )

    # ==============================================================
    # Responsive layout
    # ==============================================================

    def resizeEvent(
        self,
        event,
    ) -> None:

        super().resizeEvent(
            event
        )

        self.update_responsive_layout()

    def update_responsive_layout(
        self,
    ) -> None:

        width = self.width()

        # ----------------------------------------------------------
        # Very small
        # ----------------------------------------------------------

        if width < 650:

            self.search_box.setVisible(
                False
            )

            self.date_label.setVisible(
                False
            )

            self.subtitle_label.setVisible(
                False
            )

            self.layout_main.setContentsMargins(
                SPACING.sm,
                SPACING.xs,
                SPACING.sm,
                SPACING.xs,
            )

            self.layout_main.setSpacing(
                SPACING.xs
            )

            self.title_label.setFont(
                Typography.h2()
            )

            return

        # ----------------------------------------------------------
        # Compact
        # ----------------------------------------------------------

        if width < 850:

            self.search_box.setVisible(
                True
            )

            self.search_box.setMinimumWidth(
                140
            )

            self.search_box.setMaximumWidth(
                190
            )

            self.date_label.setVisible(
                False
            )

            self.subtitle_label.setVisible(
                False
            )

            self.layout_main.setContentsMargins(
                SPACING.md,
                SPACING.xs,
                SPACING.md,
                SPACING.xs,
            )

            self.layout_main.setSpacing(
                SPACING.xs
            )

            self.title_label.setFont(
                Typography.h2()
            )

            return

        # ----------------------------------------------------------
        # Normal
        # ----------------------------------------------------------

        self.search_box.setVisible(
            True
        )

        self.search_box.setMinimumWidth(
            180
        )

        self.search_box.setMaximumWidth(
            280
        )

        self.date_label.setVisible(
            True
        )

        self.subtitle_label.setVisible(
            True
        )

        self.layout_main.setContentsMargins(
            SPACING.lg,
            SPACING.sm,
            SPACING.lg,
            SPACING.sm,
        )

        self.layout_main.setSpacing(
            SPACING.sm
        )

        self.title_label.setFont(
            Typography.h1()
        )

    # ==============================================================
    # Page title
    # ==============================================================

    def set_page_title(
        self,
        title: str,
        subtitle: str = "",
    ) -> None:

        self.title_label.setText(
            title
        )

        self.subtitle_label.setText(
            subtitle
        )

        self.subtitle_label.setVisible(
            bool(subtitle)
        )

        self.update_responsive_layout()

    # ==============================================================
    # Search
    # ==============================================================

    def set_search_visible(
        self,
        visible: bool,
    ) -> None:

        self.search_box.setVisible(
            visible
        )

    def search_text(
        self,
    ) -> str:

        return self.search_box.text()

    def clear_search(
        self,
    ) -> None:

        self.search_box.field.clear()