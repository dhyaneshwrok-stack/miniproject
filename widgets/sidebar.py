"""
PulseMind - Sidebar
===================

Responsive application sidebar.
"""

from __future__ import annotations

from PySide6.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from config import SIDEBAR_CONFIG
from styles.theme import PALETTE, RADIUS, SPACING, Typography
from utils.icons import icon


NAV_ITEMS = [
    {
        "key": "dashboard",
        "label": "Dashboard",
        "icon": "dashboard",
    },
    {
        "key": "patients",
        "label": "Patients",
        "icon": "patients",
    },
    {
        "key": "analysis",
        "label": "ECG Analysis",
        "icon": "analysis",
    },
    {
        "key": "reports",
        "label": "Reports",
        "icon": "reports",
    },
    {
        "key": "history",
        "label": "History",
        "icon": "history",
    },
    {
        "key": "settings",
        "label": "Settings",
        "icon": "settings",
    },
    {
        "key": "about",
        "label": "About",
        "icon": "info",
    },
]


def animate_width(
    widget,
    start,
    end,
    duration,
):
    animation = QPropertyAnimation(
        widget,
        b"minimumWidth",
    )

    animation.setDuration(
        duration
    )

    animation.setStartValue(
        start
    )

    animation.setEndValue(
        end
    )

    animation.setEasingCurve(
        QEasingCurve.Type.OutCubic
    )

    animation.finished.connect(
        lambda: (
            widget.setMinimumWidth(end),
            widget.setMaximumWidth(end),
        )
    )

    widget._width_animation = animation

    widget.setMaximumWidth(
        max(
            start,
            end,
        )
    )

    animation.start()


class _NavButton(QPushButton):

    def __init__(
        self,
        key,
        label,
        icon_name,
        parent=None,
    ):

        super().__init__(
            parent
        )

        self._key = key
        self._label = label
        self._icon_name = icon_name
        self._expanded = True

        self.setCheckable(
            True
        )

        self.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.setMinimumHeight(
            46
        )

        self.setMaximumHeight(
            46
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.setFont(
            Typography.body_medium()
        )

        self._apply_style()

        self.set_expanded(
            True
        )

    def set_expanded(
        self,
        expanded,
    ):

        self._expanded = expanded

        if expanded:

            self.setText(
                f"  {self._label}"
            )

            self.setIcon(
                icon(
                    self._icon_name,
                    color=(
                        PALETTE.text_on_accent
                        if self.isChecked()
                        else PALETTE.text_secondary
                    ),
                    size=19,
                )
            )

        else:

            self.setText(
                ""
            )

            self.setIcon(
                icon(
                    self._icon_name,
                    color=(
                        PALETTE.text_on_accent
                        if self.isChecked()
                        else PALETTE.text_secondary
                    ),
                    size=19,
                )
            )

        self.setToolTip(
            ""
            if expanded
            else self._label
        )

    def _apply_style(
        self,
    ):

        self.setStyleSheet(
            f"""
            QPushButton {{
                text-align: left;
                background-color: transparent;
                color: {PALETTE.text_secondary};
                border: none;
                border-radius: {RADIUS.md}px;
                padding-left: {SPACING.md}px;
            }}

            QPushButton:hover {{
                background-color: {PALETTE.bg_card_hover};
                color: {PALETTE.text_primary};
            }}

            QPushButton:checked {{
                background-color: {PALETTE.accent};
                color: {PALETTE.text_on_accent};
            }}
            """
        )

    def refresh_icon(
        self,
    ):

        color = (
            PALETTE.text_on_accent
            if self.isChecked()
            else PALETTE.text_secondary
        )

        self.setIcon(
            icon(
                self._icon_name,
                color=color,
                size=19,
            )
        )


class Sidebar(QFrame):

    navigate_requested = Signal(str)

    logout_requested = Signal()

    toggle_requested = Signal(bool)

    def __init__(
        self,
        parent=None,
    ):

        super().__init__(
            parent
        )

        self.setObjectName(
            "Sidebar"
        )

        self._expanded = True

        self._nav_buttons = {}

        self.setMinimumWidth(
            SIDEBAR_CONFIG.expanded_width
        )

        self.setMaximumWidth(
            SIDEBAR_CONFIG.expanded_width
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding,
        )

        self.setStyleSheet(
            f"""
            #Sidebar {{
                background-color: {PALETTE.bg_secondary};
                border-right: 1px solid {PALETTE.border};
            }}
            """
        )

        root = QVBoxLayout(
            self
        )

        root.setContentsMargins(
            SPACING.md,
            SPACING.lg,
            SPACING.md,
            SPACING.lg,
        )

        root.setSpacing(
            SPACING.xs
        )

        root.addWidget(
            self._build_brand()
        )

        root.addSpacing(
            SPACING.lg
        )

        self._nav_group = QButtonGroup(
            self
        )

        self._nav_group.setExclusive(
            True
        )

        for index, item in enumerate(
            NAV_ITEMS
        ):

            button = _NavButton(
                item["key"],
                item["label"],
                item["icon"],
            )

            button.clicked.connect(
                lambda _checked,
                key=item["key"]:
                self._on_nav_clicked(
                    key
                )
            )

            self._nav_group.addButton(
                button
            )

            self._nav_buttons[
                item["key"]
            ] = button

            root.addWidget(
                button
            )

            if index == 0:

                button.setChecked(
                    True
                )

                button.refresh_icon()

        root.addStretch(
            1
        )

        divider = QFrame()

        divider.setFixedHeight(
            1
        )

        divider.setStyleSheet(
            f"""
            background-color: {PALETTE.border};
            """
        )

        root.addWidget(
            divider
        )

        root.addSpacing(
            SPACING.xs
        )

        # ----------------------------------------------------------
        # Collapse
        # ----------------------------------------------------------

        self._collapse_btn = QPushButton(
            "  Collapse"
        )

        self._collapse_btn.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self._collapse_btn.setFixedHeight(
            40
        )

        self._collapse_btn.setFont(
            Typography.body_small()
        )

        self._collapse_btn.setIcon(
            icon(
                "chevron_left",
                color=PALETTE.text_secondary,
                size=16,
            )
        )

        self._collapse_btn.setStyleSheet(
            f"""
            QPushButton {{
                text-align: left;
                background-color: transparent;
                color: {PALETTE.text_secondary};
                border: none;
                border-radius: {RADIUS.md}px;
                padding-left: {SPACING.md}px;
            }}

            QPushButton:hover {{
                background-color: {PALETTE.bg_card_hover};
                color: {PALETTE.text_primary};
            }}
            """
        )

        self._collapse_btn.clicked.connect(
            self.toggle_collapsed
        )

        root.addWidget(
            self._collapse_btn
        )

        # ----------------------------------------------------------
        # Logout
        # ----------------------------------------------------------

        logout_btn = _NavButton(
            "logout",
            "Logout",
            "logout",
        )

        logout_btn.setCheckable(
            False
        )

        logout_btn.clicked.connect(
            self.logout_requested.emit
        )

        logout_btn.setStyleSheet(
            logout_btn.styleSheet()
            + f"""
            QPushButton:hover {{
                background-color: rgba(
                    229,
                    57,
                    53,
                    0.14
                );
                color: {PALETTE.danger};
            }}
            """
        )

        self._logout_btn = logout_btn

        root.addWidget(
            logout_btn
        )

    # ==============================================================
    # Brand
    # ==============================================================

    def _build_brand(
        self,
    ):

        brand = QWidget()

        layout = QHBoxLayout(
            brand
        )

        layout.setContentsMargins(
            SPACING.xs,
            0,
            0,
            0,
        )

        layout.setSpacing(
            SPACING.sm
        )

        mark = QLabel()

        mark.setFixedSize(
            36,
            36,
        )

        mark.setPixmap(
            icon(
                "heartbeat",
                color=PALETTE.text_on_accent,
                size=18,
            ).pixmap(
                18,
                18,
            )
        )

        mark.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        mark.setStyleSheet(
            f"""
            background-color: {PALETTE.accent};
            border-radius: {RADIUS.sm}px;
            """
        )

        layout.addWidget(
            mark
        )

        text_box = QVBoxLayout()

        text_box.setSpacing(
            0
        )

        name_label = QLabel(
            "PulseMind"
        )

        name_label.setFont(
            Typography.h3()
        )

        name_label.setStyleSheet(
            f"color: {PALETTE.text_primary};"
        )

        tagline_label = QLabel(
            "ECG Analysis"
        )

        tagline_label.setFont(
            Typography.caption()
        )

        tagline_label.setStyleSheet(
            f"color: {PALETTE.text_secondary};"
        )

        text_box.addWidget(
            name_label
        )

        text_box.addWidget(
            tagline_label
        )

        self._brand_text_widgets = (
            name_label,
            tagline_label,
        )

        layout.addLayout(
            text_box
        )

        layout.addStretch(
            1
        )

        self._brand_container = brand

        return brand

    # ==============================================================
    # Navigation
    # ==============================================================

    def _on_nav_clicked(
        self,
        key,
    ):

        for button in self._nav_buttons.values():

            button.refresh_icon()

        self.navigate_requested.emit(
            key
        )

    def set_active(
        self,
        key,
    ):

        button = self._nav_buttons.get(
            key
        )

        if button is not None:

            button.setChecked(
                True
            )

            for btn in self._nav_buttons.values():

                btn.refresh_icon()

    # ==============================================================
    # Collapse
    # ==============================================================

    def toggle_collapsed(
        self,
    ):

        self.set_collapsed(
            self._expanded
        )

    def is_collapsed(
        self,
    ):

        return not self._expanded

    def set_collapsed(
        self,
        collapsed,
    ):

        self._expanded = not collapsed

        start = self.width()

        if start <= 0:

            start = (
                SIDEBAR_CONFIG.expanded_width
                if not collapsed
                else SIDEBAR_CONFIG.collapsed_width
            )

        end = (
            SIDEBAR_CONFIG.collapsed_width
            if collapsed
            else SIDEBAR_CONFIG.expanded_width
        )

        animate_width(
            self,
            start,
            end,
            SIDEBAR_CONFIG.animation_duration_ms,
        )

        for button in self._nav_buttons.values():

            button.set_expanded(
                not collapsed
            )

        self._logout_btn.set_expanded(
            not collapsed
        )

        self._collapse_btn.setText(
            ""
            if collapsed
            else "  Collapse"
        )

        self._collapse_btn.setIcon(
            icon(
                "chevron_right"
                if collapsed
                else "chevron_left",
                color=PALETTE.text_secondary,
                size=16,
            )
        )

        for widget in self._brand_text_widgets:

            widget.setVisible(
                not collapsed
            )

        self.toggle_requested.emit(
            collapsed
        )