"""
PulseMind - Base Page
=====================

Common responsive page container used by all application views.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from styles.theme import PALETTE, SPACING, Typography


class BasePage(QWidget):
    """
    Base class for all PulseMind pages.

    Provides:
    - Page title
    - Page subtitle
    - Responsive vertical content
    - Vertical scrolling
    - Horizontal scrolling when a view genuinely needs it
    """

    page_key = ""
    page_title = ""
    page_subtitle = ""

    def __init__(
        self,
        parent=None,
    ) -> None:

        super().__init__(
            parent
        )

        self.setObjectName(
            "BasePage"
        )

        self._build_base_ui()

        self.build()

    # ==============================================================
    # Build
    # ==============================================================

    def _build_base_ui(self) -> None:

        outer_layout = QVBoxLayout(
            self
        )

        outer_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        outer_layout.setSpacing(
            0
        )

        # ----------------------------------------------------------
        # Scroll area
        # ----------------------------------------------------------

        self.scroll_area = QScrollArea()

        self.scroll_area.setObjectName(
            "PageScrollArea"
        )

        self.scroll_area.setWidgetResizable(
            True
        )

        # IMPORTANT:
        # Do not completely disable horizontal scrolling.
        # Some views contain tables or ECG controls that cannot
        # become narrower than a readable size.

        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.scroll_area.setFrameShape(
            QScrollArea.Shape.NoFrame
        )

        self.scroll_area.setWidget(
            self._create_content_widget()
        )

        outer_layout.addWidget(
            self.scroll_area
        )

    # ==============================================================
    # Content widget
    # ==============================================================

    def _create_content_widget(self) -> QWidget:

        self.content_widget = QWidget()

        self.content_widget.setObjectName(
            "PageContent"
        )

        self.content_layout = QVBoxLayout(
            self.content_widget
        )

        self.content_layout.setContentsMargins(
            SPACING.xl,
            SPACING.lg,
            SPACING.xl,
            SPACING.xl,
        )

        self.content_layout.setSpacing(
            SPACING.lg
        )

        # ----------------------------------------------------------
        # Page heading
        # ----------------------------------------------------------

        self.title_label = QLabel(
            self.page_title
        )

        self.title_label.setObjectName(
            "PageTitle"
        )

        self.title_label.setFont(
            Typography.h1()
        )

        self.title_label.setStyleSheet(
            f"""
            color: {PALETTE.text_primary};
            """
        )

        self.title_label.setWordWrap(
            True
        )

        self.content_layout.addWidget(
            self.title_label
        )

        # ----------------------------------------------------------
        # Page subtitle
        # ----------------------------------------------------------

        if self.page_subtitle:

            self.subtitle_label = QLabel(
                self.page_subtitle
            )

            self.subtitle_label.setObjectName(
                "PageSubtitle"
            )

            self.subtitle_label.setFont(
                Typography.body()
            )

            self.subtitle_label.setStyleSheet(
                f"""
                color: {PALETTE.text_secondary};
                """
            )

            self.subtitle_label.setWordWrap(
                True
            )

            self.content_layout.addWidget(
                self.subtitle_label
            )

        else:

            self.subtitle_label = None

        return self.content_widget

    # ==============================================================
    # Responsive hook
    # ==============================================================

    def update_responsive_layout(self) -> None:
        """
        Optional hook for individual pages.

        Pages with special layouts such as Dashboard, Analysis,
        Patients and Reports can override this method.
        """

        # Default page does not need any special action.
        pass

    # ==============================================================
    # Build hook
    # ==============================================================

    def build(self) -> None:
        """
        Child classes implement their UI here.
        """
        pass

    # ==============================================================
    # Common helpers
    # ==============================================================

    def add_spacing(
        self,
        amount: int = None,
    ) -> None:

        if amount is None:
            amount = SPACING.md

        self.content_layout.addSpacing(
            amount
        )

    def add_stretch(self) -> None:

        self.content_layout.addStretch(
            1
        )