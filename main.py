"""
PulseMind - Application Entry Point
====================================

Responsive application shell for PulseMind.

This file handles:
- Application startup
- Login
- Main window
- Sidebar
- Top bar
- Page switching
- Window resizing
- Responsive sidebar behavior
- Logout
"""

from __future__ import annotations

import sys

from PySide6.QtCore import QPoint, QSettings, Qt
from PySide6.QtGui import QColor, QFontDatabase, QGuiApplication
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from config import APP_INFO, SettingsKeys, WINDOW_CONFIG
from database.database import database_manager
from styles.theme import PALETTE
from viewmodels.navigation_viewmodel import NavigationViewModel

from views.about import AboutPage
from views.analysis import AnalysisPage
from views.dashboard import DashboardPage
from views.history import HistoryPage
from views.login import LoginDialog
from views.patients import PatientsPage
from views.reports import ReportsPage
from views.settings import SettingsPage

from widgets.sidebar import Sidebar
from widgets.titlebar import TitleBar
from widgets.topbar import TopBar


PAGE_CLASSES = [
    DashboardPage,
    PatientsPage,
    AnalysisPage,
    ReportsPage,
    HistoryPage,
    SettingsPage,
    AboutPage,
]


RESIZE_MARGIN = WINDOW_CONFIG.resize_margin

LOGOUT_EXIT_CODE = 100

# ---------------------------------------------------------------------
# Responsive breakpoints
# ---------------------------------------------------------------------

# Below this width the sidebar should collapse.
SIDEBAR_COLLAPSE_WIDTH = 1050

# Below this width the application becomes very compact.
COMPACT_WIDTH = 850


class MainWindow(QMainWindow):
    """
    Main PulseMind application window.

    The window automatically changes the sidebar state when the
    available window width becomes smaller.
    """

    def __init__(self, user=None) -> None:
        super().__init__()

        self.current_user = user

        self.setWindowTitle(APP_INFO.name)

        self.setMinimumSize(
            WINDOW_CONFIG.min_width,
            WINDOW_CONFIG.min_height,
        )

        self.resize(
            WINDOW_CONFIG.default_width,
            WINDOW_CONFIG.default_height,
        )

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Window
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setMouseTracking(True)

        self._settings = QSettings()

        self._nav_vm = NavigationViewModel(self)

        self._resize_edge: Qt.Edges = Qt.Edge(0)

        self._drag_active = False

        # Prevent repeated sidebar changes while resizing.
        self._responsive_sidebar_state = None

        self._build_ui()
        self._wire_signals()
        self._restore_window_state()

        # Apply responsive state after the window has its real size.
        self._update_responsive_layout()

    # ==============================================================
    # Build UI
    # ==============================================================

    def _build_ui(self) -> None:
        root = QWidget()
        root.setMouseTracking(True)

        root_layout = QVBoxLayout(root)

        root_layout.setContentsMargins(
            WINDOW_CONFIG.resize_margin,
            WINDOW_CONFIG.resize_margin,
            WINDOW_CONFIG.resize_margin,
            WINDOW_CONFIG.resize_margin,
        )

        self.setCentralWidget(root)

        # ----------------------------------------------------------
        # Main surface
        # ----------------------------------------------------------

        self.container = QFrame()

        self.container.setObjectName(
            "CentralSurface"
        )

        self.container.setMouseTracking(True)

        self.container.setStyleSheet(
            f"""
            #CentralSurface {{
                background-color: {PALETTE.bg_primary};
                border-radius: {WINDOW_CONFIG.corner_radius}px;
                border: 1px solid {PALETTE.border};
            }}
            """
        )

        shadow = QGraphicsDropShadowEffect(
            self.container
        )

        shadow.setBlurRadius(48)
        shadow.setOffset(0, 12)

        shadow.setColor(
            QColor(0, 0, 0, 160)
        )

        self.container.setGraphicsEffect(
            shadow
        )

        root_layout.addWidget(
            self.container
        )

        container_layout = QVBoxLayout(
            self.container
        )

        container_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        container_layout.setSpacing(0)

        # ----------------------------------------------------------
        # Title bar
        # ----------------------------------------------------------

        self.title_bar = TitleBar()

        container_layout.addWidget(
            self.title_bar
        )

        # ----------------------------------------------------------
        # Body
        # ----------------------------------------------------------

        body = QWidget()

        body.setObjectName(
            "MainBody"
        )

        body_layout = QHBoxLayout(body)

        body_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        body_layout.setSpacing(0)

        container_layout.addWidget(
            body
        )

        # ----------------------------------------------------------
        # Sidebar
        # ----------------------------------------------------------

        self.sidebar = Sidebar()

        body_layout.addWidget(
            self.sidebar
        )

        # ----------------------------------------------------------
        # Content area
        # ----------------------------------------------------------

        content = QWidget()

        content.setObjectName(
            "MainContent"
        )

        content_layout = QVBoxLayout(
            content
        )

        content_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        content_layout.setSpacing(0)

        body_layout.addWidget(
            content,
            stretch=1,
        )

        # ----------------------------------------------------------
        # Top bar
        # ----------------------------------------------------------

        self.top_bar = TopBar()

        content_layout.addWidget(
            self.top_bar
        )

        # ----------------------------------------------------------
        # Pages
        # ----------------------------------------------------------

        self.stack = QStackedWidget()

        self.stack.setObjectName(
            "PageStack"
        )

        self.stack.setStyleSheet(
            f"""
            QStackedWidget#PageStack {{
                background-color: {PALETTE.bg_primary};
            }}
            """
        )

        content_layout.addWidget(
            self.stack,
            stretch=1,
        )

        # ----------------------------------------------------------
        # Create pages
        # ----------------------------------------------------------

        self._pages: dict[str, QWidget] = {}

        for page_cls in PAGE_CLASSES:

            page = page_cls()

            self._pages[
                page_cls.page_key
            ] = page

            self.stack.addWidget(
                page
            )

        self._show_page(
            self._nav_vm.active_page
        )

    # ==============================================================
    # Signals
    # ==============================================================

    def _wire_signals(self) -> None:

        self.title_bar.minimize_requested.connect(
            self.showMinimized
        )

        self.title_bar.maximize_requested.connect(
            self._toggle_maximize
        )

        self.title_bar.close_requested.connect(
            self.close
        )

        self.sidebar.navigate_requested.connect(
            self._nav_vm.set_active_page
        )

        self.sidebar.toggle_requested.connect(
            self._nav_vm.set_sidebar_collapsed
        )

        self.sidebar.logout_requested.connect(
            self._on_logout_requested
        )

        self._nav_vm.active_page_changed.connect(
            self._show_page
        )

        # Send global search text to pages that support searching.
        self.top_bar.search_changed.connect(
            self._on_global_search
        )

    def _on_global_search(self, text: str) -> None:
        """Forward the top-bar search text to searchable pages."""

        query = text or ""

        for page in self._pages.values():
            if hasattr(page, "set_search_text"):
                page.set_search_text(query)

    # ==============================================================
    # Restore window state
    # ==============================================================

    def _restore_window_state(self) -> None:

        collapsed = bool(
            self._settings.value(
                SettingsKeys.SIDEBAR_COLLAPSED,
                False,
                type=bool,
            )
        )

        if collapsed:

            self.sidebar.set_collapsed(
                True
            )

            self._nav_vm.set_sidebar_collapsed(
                True
            )

    # ==============================================================
    # Responsive layout
    # ==============================================================

    def _update_responsive_layout(self) -> None:
        """
        Automatically collapse/expand the sidebar depending on
        the available window width.

        Manual user preference is still respected when the window
        is large enough.
        """

        if self.isMaximized():

            width = self.screen().availableGeometry().width()

        else:

            width = self.width()

        should_collapse = (
            width < SIDEBAR_COLLAPSE_WIDTH
        )

        desired_state = should_collapse

        if (
            desired_state
            == self._responsive_sidebar_state
        ):
            return

        self._responsive_sidebar_state = desired_state

        if should_collapse:

            if not self.sidebar.is_collapsed():

                self.sidebar.set_collapsed(
                    True
                )

        else:

            # Restore the user's saved preference.
            saved_collapsed = bool(
                self._settings.value(
                    SettingsKeys.SIDEBAR_COLLAPSED,
                    False,
                    type=bool,
                )
            )

            if saved_collapsed:

                self.sidebar.set_collapsed(
                    True
                )

            else:

                self.sidebar.set_collapsed(
                    False
                )

        # Give the current page a chance to react to the new width.
        current_page = self.stack.currentWidget()

        if current_page is not None:

            if hasattr(
                current_page,
                "update_responsive_layout",
            ):

                current_page.update_responsive_layout()

    # ==============================================================
    # Page switching
    # ==============================================================

    def _show_page(
        self,
        key: str,
    ) -> None:

        page = self._pages.get(
            key
        )

        if page is None:
            return

        self.stack.setCurrentWidget(
            page
        )

        self.sidebar.set_active(
            key
        )

        self.top_bar.set_page_title(
            page.page_title,
            page.page_subtitle,
        )

        if (
            key == "history"
            and hasattr(
                page,
                "refresh",
            )
        ):

            page.refresh()

        if (
            key == "reports"
            and hasattr(
                page,
                "refresh",
            )
        ):

            page.refresh()

        # Keep the current global search active when changing pages.
        if hasattr(page, "set_search_text"):
            page.set_search_text(self.top_bar.search_text())

        if hasattr(
            page,
            "update_responsive_layout",
        ):

            page.update_responsive_layout()

    # ==============================================================
    # Logout
    # ==============================================================

    def _on_logout_requested(self) -> None:

        self.hide()

        QApplication.exit(
            LOGOUT_EXIT_CODE
        )

    # ==============================================================
    # Window controls
    # ==============================================================

    def _toggle_maximize(self) -> None:

        if self.isMaximized():

            self.showNormal()

        else:

            self.showMaximized()

        self._update_responsive_layout()

    # ==============================================================
    # Window resize
    # ==============================================================

    def resizeEvent(
        self,
        event,
    ) -> None:

        super().resizeEvent(
            event
        )

        self._update_responsive_layout()

    # ==============================================================
    # Close
    # ==============================================================

    def closeEvent(
        self,
        event,
    ) -> None:

        self._settings.setValue(
            SettingsKeys.SIDEBAR_COLLAPSED,
            self._nav_vm.sidebar_collapsed,
        )

        self._settings.setValue(
            SettingsKeys.WINDOW_MAXIMIZED,
            self.isMaximized(),
        )

        if not self.isMaximized():

            self._settings.setValue(
                SettingsKeys.WINDOW_GEOMETRY,
                self.saveGeometry(),
            )

        database_manager.close()

        super().closeEvent(
            event
        )

    # ==============================================================
    # Frameless edge resize
    # ==============================================================

    def _edge_at(
        self,
        pos: QPoint,
    ) -> Qt.Edges:

        edges = Qt.Edge(0)

        if self.isMaximized():
            return edges

        rect = self.rect()

        if pos.x() <= RESIZE_MARGIN:

            edges |= Qt.Edge.LeftEdge

        elif pos.x() >= (
            rect.width()
            - RESIZE_MARGIN
        ):

            edges |= Qt.Edge.RightEdge

        if pos.y() <= RESIZE_MARGIN:

            edges |= Qt.Edge.TopEdge

        elif pos.y() >= (
            rect.height()
            - RESIZE_MARGIN
        ):

            edges |= Qt.Edge.BottomEdge

        return edges

    def _cursor_for_edges(
        self,
        edges: Qt.Edges,
    ) -> Qt.CursorShape:

        horizontal = bool(
            edges
            & (
                Qt.Edge.LeftEdge
                | Qt.Edge.RightEdge
            )
        )

        vertical = bool(
            edges
            & (
                Qt.Edge.TopEdge
                | Qt.Edge.BottomEdge
            )
        )

        if (
            edges & Qt.Edge.LeftEdge
            and edges & Qt.Edge.TopEdge
        ) or (
            edges & Qt.Edge.RightEdge
            and edges & Qt.Edge.BottomEdge
        ):

            return Qt.CursorShape.SizeFDiagCursor

        if (
            edges & Qt.Edge.RightEdge
            and edges & Qt.Edge.TopEdge
        ) or (
            edges & Qt.Edge.LeftEdge
            and edges & Qt.Edge.BottomEdge
        ):

            return Qt.CursorShape.SizeBDiagCursor

        if horizontal:

            return Qt.CursorShape.SizeHorCursor

        if vertical:

            return Qt.CursorShape.SizeVerCursor

        return Qt.CursorShape.ArrowCursor

    def mousePressEvent(
        self,
        event,
    ) -> None:

        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):

            edges = self._edge_at(
                event.position().toPoint()
            )

            if edges:

                self._resize_edge = edges

                handle = self.windowHandle()

                if handle is not None:

                    handle.startSystemResize(
                        edges
                    )

                event.accept()

                return

        super().mousePressEvent(
            event
        )

    def mouseMoveEvent(
        self,
        event,
    ) -> None:

        if not self._drag_active:

            edges = self._edge_at(
                event.position().toPoint()
            )

            self.setCursor(
                self._cursor_for_edges(
                    edges
                )
            )

        super().mouseMoveEvent(
            event
        )


# ==============================================================
# Fonts
# ==============================================================

def _load_fonts() -> None:

    from config import FONTS_DIR

    if not FONTS_DIR.exists():
        return

    for font_file in FONTS_DIR.glob(
        "*.[ot]tf"
    ):

        QFontDatabase.addApplicationFont(
            str(font_file)
        )


# ==============================================================
# Stylesheet
# ==============================================================

def _load_stylesheet(
    app: QApplication,
) -> None:

    from config import STYLES_DIR

    qss_path = (
        STYLES_DIR
        / "dark.qss"
    )

    if qss_path.exists():

        app.setStyleSheet(
            qss_path.read_text(
                encoding="utf-8"
            )
        )


# ==============================================================
# Application entry point
# ==============================================================

def main() -> int:

    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(
        sys.argv
    )

    app.setOrganizationName(
        APP_INFO.organization
    )

    app.setApplicationName(
        APP_INFO.name
    )

    app.setApplicationVersion(
        APP_INFO.version
    )

    _load_fonts()

    _load_stylesheet(
        app
    )

    database_manager.initialize()

    # ----------------------------------------------------------
    # Login → Application → Logout → Login
    # ----------------------------------------------------------

    while True:

        login = LoginDialog()

        login_result = login.exec()

        if (
            login_result
            != QDialog.DialogCode.Accepted
        ):

            break

        user = login.user

        window = MainWindow(
            user=user
        )

        window.show()

        exit_code = app.exec()

        if exit_code == LOGOUT_EXIT_CODE:

            continue

        break

    database_manager.close()

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )