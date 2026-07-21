"""
PulseMind - Custom Title Bar
===============================

Replaces the OS window chrome with a draggable, custom-styled title
bar carrying minimize / maximize / close controls, matching the
frameless-window requirement from the design brief.
"""

from __future__ import annotations

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from config import APP_INFO
from styles.theme import PALETTE, RADIUS, SPACING, Typography
from utils.icons import icon
from widgets.buttons import IconButton


class TitleBar(QFrame):
    """Frameless window title bar: drag-to-move + window controls."""

    minimize_requested = Signal()
    maximize_requested = Signal()
    close_requested = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("TitleBar")
        self.setFixedHeight(52)
        self.setStyleSheet(f"""
            #TitleBar {{
                background-color: {PALETTE.bg_secondary};
                border-top-left-radius: {RADIUS.lg}px;
                border-top-right-radius: {RADIUS.lg}px;
                border-bottom: 1px solid {PALETTE.border};
            }}
        """)

        self._drag_position: QPoint | None = None

        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACING.md, 0, SPACING.sm, 0)
        layout.setSpacing(SPACING.sm)

        mark = QLabel()
        mark.setFixedSize(26, 26)
        mark.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mark.setPixmap(icon("heartbeat", color=PALETTE.text_on_accent, size=14).pixmap(14, 14))
        mark.setStyleSheet(f"background-color: {PALETTE.accent}; border-radius: 7px;")
        layout.addWidget(mark)

        title = QLabel(APP_INFO.name)
        title.setFont(Typography.body_medium())
        title.setStyleSheet(f"color: {PALETTE.text_primary};")
        layout.addWidget(title)

        tagline = QLabel(f"  •  {APP_INFO.tagline}")
        tagline.setFont(Typography.caption())
        tagline.setStyleSheet(f"color: {PALETTE.text_muted};")
        layout.addWidget(tagline)

        layout.addStretch(1)

        self.minimize_btn = IconButton(icon("minimize", color=PALETTE.text_secondary, size=14))
        self.minimize_btn.clicked.connect(self.minimize_requested.emit)
        layout.addWidget(self.minimize_btn)

        self.maximize_btn = IconButton(icon("maximize", color=PALETTE.text_secondary, size=13))
        self.maximize_btn.clicked.connect(self.maximize_requested.emit)
        layout.addWidget(self.maximize_btn)

        self.close_btn = IconButton(
            icon("close", color=PALETTE.text_secondary, size=14), danger_hover=True
        )
        self.close_btn.clicked.connect(self.close_requested.emit)
        layout.addWidget(self.close_btn)

    # -- Window dragging -------------------------------------------------

    def mousePressEvent(self, event) -> None:  # noqa: N802 (Qt override)
        if event.button() == Qt.MouseButton.LeftButton:
            window = self.window()
            self._drag_position = (
                event.globalPosition().toPoint() - window.frameGeometry().topLeft()
            )
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:  # noqa: N802 (Qt override)
        if self._drag_position is not None and event.buttons() & Qt.MouseButton.LeftButton:
            window = self.window()
            window.move(event.globalPosition().toPoint() - self._drag_position)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802 (Qt override)
        self._drag_position = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:  # noqa: N802 (Qt override)
        if event.button() == Qt.MouseButton.LeftButton:
            self.maximize_requested.emit()
        super().mouseDoubleClickEvent(event)
