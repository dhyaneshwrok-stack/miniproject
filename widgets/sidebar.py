"""
PulseMind - Sidebar Navigation
=================================

Collapsible sidebar with animated expand/collapse, hover states, and a
persistent selected-page highlight. Purely a navigation surface -- it
knows nothing about page content, only which key was selected.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup, QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout,
    QWidget,
)

from config import NAV_ITEMS, SIDEBAR_CONFIG
from styles.theme import PALETTE, RADIUS, SPACING, Typography
from utils.animations import animate_width
from utils.icons import icon


class _NavButton(QPushButton):
    """A single, checkable sidebar navigation entry."""

    def __init__(self, key: str, label: str, icon_name: str, parent=None) -> None:
        super().__init__(parent)
        self.key = key
        self._label = label
        self._icon_name = icon_name
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(46)
        self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.setFont(Typography.body_medium())
        self._apply_content(expanded=True)
        self._apply_style()

    def _apply_content(self, expanded: bool) -> None:
        self.setText(f"   {self._label}" if expanded else "")
        self.setToolTip("" if expanded else self._label)
        color = PALETTE.text_on_accent if self.isChecked() else PALETTE.text_secondary
        self.setIcon(icon(self._icon_name, color=color, size=19))
        self.setIconSize(self.iconSize())
        self.setStyleSheet(self.styleSheet())  # force repaint of icon color region

    def set_expanded(self, expanded: bool) -> None:
        self._apply_content(expanded)
        alignment = Qt.AlignmentFlag.AlignLeft if expanded else Qt.AlignmentFlag.AlignCenter
        self.setStyleSheet(self.styleSheet())
        self._alignment = alignment

    def _apply_style(self) -> None:
        self.setStyleSheet(f"""
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
        """)

    def refresh_icon(self) -> None:
        color = PALETTE.text_on_accent if self.isChecked() else PALETTE.text_secondary
        self.setIcon(icon(self._icon_name, color=color, size=19))


class Sidebar(QFrame):
    """Application sidebar: brand header, nav list, and logout footer."""

    navigate_requested = Signal(str)
    logout_requested = Signal()
    toggle_requested = Signal(bool)  # emits new collapsed state

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self._expanded = True
        self._nav_buttons: dict[str, _NavButton] = {}

        self.setMinimumWidth(SIDEBAR_CONFIG.expanded_width)
        self.setMaximumWidth(SIDEBAR_CONFIG.expanded_width)
        self.setStyleSheet(f"""
            #Sidebar {{
                background-color: {PALETTE.bg_secondary};
                border-right: 1px solid {PALETTE.border};
            }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(SPACING.md, SPACING.lg, SPACING.md, SPACING.lg)
        root.setSpacing(SPACING.xs)

        root.addWidget(self._build_brand())
        root.addSpacing(SPACING.lg)

        self._nav_group = QButtonGroup(self)
        self._nav_group.setExclusive(True)

        for index, item in enumerate(NAV_ITEMS):
            button = _NavButton(item["key"], item["label"], item["icon"])
            button.clicked.connect(lambda _checked, k=item["key"]: self._on_nav_clicked(k))
            self._nav_group.addButton(button)
            self._nav_buttons[item["key"]] = button
            root.addWidget(button)
            if index == 0:
                button.setChecked(True)
                button.refresh_icon()

        root.addStretch(1)

        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet(f"background-color: {PALETTE.border};")
        root.addWidget(divider)
        root.addSpacing(SPACING.xs)

        self._collapse_btn = QPushButton("  Collapse")
        self._collapse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._collapse_btn.setFixedHeight(40)
        self._collapse_btn.setFont(Typography.body_small())
        self._collapse_btn.setIcon(icon("chevron_left", color=PALETTE.text_secondary, size=16))
        self._collapse_btn.setStyleSheet(f"""
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
        """)
        self._collapse_btn.clicked.connect(self.toggle_collapsed)
        root.addWidget(self._collapse_btn)

        logout_btn = _NavButton("logout", "Logout", "logout")
        logout_btn.setCheckable(False)
        logout_btn.clicked.connect(self.logout_requested.emit)
        logout_btn.setStyleSheet(logout_btn.styleSheet() + f"""
            QPushButton:hover {{ background-color: rgba(229, 57, 53, 0.14); color: {PALETTE.danger}; }}
        """)
        self._logout_btn = logout_btn
        root.addWidget(logout_btn)

    def _build_brand(self) -> QWidget:
        brand = QWidget()
        layout = QHBoxLayout(brand)
        layout.setContentsMargins(SPACING.xs, 0, 0, 0)
        layout.setSpacing(SPACING.sm)

        mark = QLabel()
        mark.setFixedSize(36, 36)
        mark.setPixmap(icon("heartbeat", color=PALETTE.text_on_accent, size=18).pixmap(18, 18))
        mark.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mark.setStyleSheet(f"""
            background-color: {PALETTE.accent};
            border-radius: {RADIUS.sm}px;
        """)
        layout.addWidget(mark)

        text_box = QVBoxLayout()
        text_box.setSpacing(0)
        name_label = QLabel("PulseMind")
        name_label.setFont(Typography.h3())
        name_label.setStyleSheet(f"color: {PALETTE.text_primary};")
        tagline_label = QLabel("ECG Analysis")
        tagline_label.setFont(Typography.caption())
        tagline_label.setStyleSheet(f"color: {PALETTE.text_secondary};")
        text_box.addWidget(name_label)
        text_box.addWidget(tagline_label)

        self._brand_text_widgets = (name_label, tagline_label)
        layout.addLayout(text_box)
        layout.addStretch(1)
        self._brand_container = brand
        return brand

    def _on_nav_clicked(self, key: str) -> None:
        for k, btn in self._nav_buttons.items():
            btn.refresh_icon()
        self.navigate_requested.emit(key)

    def set_active(self, key: str) -> None:
        button = self._nav_buttons.get(key)
        if button is not None:
            button.setChecked(True)
            for btn in self._nav_buttons.values():
                btn.refresh_icon()

    def toggle_collapsed(self) -> None:
        self.set_collapsed(self._expanded)

    def set_collapsed(self, collapsed: bool) -> None:
        self._expanded = not collapsed
        start = self.minimumWidth()
        end = SIDEBAR_CONFIG.collapsed_width if collapsed else SIDEBAR_CONFIG.expanded_width
        animate_width(self, start, end, SIDEBAR_CONFIG.animation_duration_ms)

        for button in self._nav_buttons.values():
            button.set_expanded(not collapsed)
        self._logout_btn.set_expanded(not collapsed)

        self._collapse_btn.setText("" if collapsed else "  Collapse")
        self._collapse_btn.setIcon(
            icon("chevron_right" if collapsed else "chevron_left",
                 color=PALETTE.text_secondary, size=16)
        )

        for widget in self._brand_text_widgets:
            widget.setVisible(not collapsed)

        self.toggle_requested.emit(collapsed)
