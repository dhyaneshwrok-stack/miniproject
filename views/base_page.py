"""
PulseMind - Base Page
========================

Every page in Phase 1 (Dashboard, Patients, ECG Analysis, Reports,
History, Settings, About) shares the same shell: a scrollable content
area with consistent spacing, ready to host stat cards, info cards, or
an empty state. Subclassing this keeps every page visually consistent
without duplicating layout code.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

from styles.theme import SPACING


class BasePage(QWidget):
    """Common scrollable shell for a top-level navigation page."""

    #: Sidebar / navigation key this page corresponds to.
    page_key: str = ""
    #: Title shown in the top bar when this page is active.
    page_title: str = ""
    #: Subtitle shown beneath the title in the top bar.
    page_subtitle: str = ""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        outer.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)

        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(
            SPACING.xl, SPACING.lg, SPACING.xl, SPACING.xl
        )
        self.content_layout.setSpacing(SPACING.lg)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.build()

    def build(self) -> None:
        """Subclasses override this to populate ``self.content_layout``."""
        raise NotImplementedError
