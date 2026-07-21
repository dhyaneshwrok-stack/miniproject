"""
PulseMind - Application Entry Point
======================================

Boots the QApplication, loads global fonts and the dark stylesheet,
initializes the SQLite connection, and shows the custom frameless
MainWindow. This file intentionally contains no business logic --
only wiring.
"""

from __future__ import annotations

import sys

from PySide6.QtCore import QPoint, QSettings, Qt
from PySide6.QtGui import QColor, QFontDatabase, QGuiApplication
from PySide6.QtWidgets import (
    QApplication, QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
    QMainWindow, QStackedWidget, QVBoxLayout, QWidget,
)

from config import APP_INFO, SettingsKeys, WINDOW_CONFIG
from database.database import database_manager
from styles.theme import PALETTE
from viewmodels.navigation_viewmodel import NavigationViewModel
from views.about import AboutPage
from views.analysis import AnalysisPage
from views.dashboard import DashboardPage
from views.history import HistoryPage
from views.patients import PatientsPage
from views.reports import ReportsPage
from views.settings import SettingsPage
from widgets.sidebar import Sidebar
from widgets.titlebar import TitleBar
from widgets.topbar import TopBar

PAGE_CLASSES = [
    DashboardPage, PatientsPage, AnalysisPage, ReportsPage,
    HistoryPage, SettingsPage, AboutPage,
]

RESIZE_MARGIN = WINDOW_CONFIG.resize_margin


class MainWindow(QMainWindow):
    """Custom frameless application window with rounded corners.

    The real QMainWindow is fully transparent; a rounded, shadowed
    ``self.container`` widget draws the visible surface. This is the
    standard technique for achieving a rounded, shadowed frameless
    window in Qt Widgets.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(APP_INFO.name)
        self.setMinimumSize(WINDOW_CONFIG.min_width, WINDOW_CONFIG.min_height)
        self.resize(WINDOW_CONFIG.default_width, WINDOW_CONFIG.default_height)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self._settings = QSettings()
        self._nav_vm = NavigationViewModel(self)
        self._resize_edge: Qt.Edges = Qt.Edge(0)
        self._drag_active = False

        self._build_ui()
        self._wire_signals()
        self._restore_window_state()

    # -- UI construction ---------------------------------------------------

    def _build_ui(self) -> None:
        root = QWidget()
        root.setMouseTracking(True)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(WINDOW_CONFIG.resize_margin,
                                        WINDOW_CONFIG.resize_margin,
                                        WINDOW_CONFIG.resize_margin,
                                        WINDOW_CONFIG.resize_margin)
        self.setCentralWidget(root)

        self.container = QFrame()
        self.container.setObjectName("CentralSurface")
        self.container.setMouseTracking(True)
        self.container.setStyleSheet(f"""
            #CentralSurface {{
                background-color: {PALETTE.bg_primary};
                border-radius: {WINDOW_CONFIG.corner_radius}px;
                border: 1px solid {PALETTE.border};
            }}
        """)
        shadow = QGraphicsDropShadowEffect(self.container)
        shadow.setBlurRadius(48)
        shadow.setOffset(0, 12)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.container.setGraphicsEffect(shadow)
        root_layout.addWidget(self.container)

        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        self.title_bar = TitleBar()
        container_layout.addWidget(self.title_bar)

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        container_layout.addWidget(body, stretch=1)

        self.sidebar = Sidebar()
        body_layout.addWidget(self.sidebar)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        body_layout.addWidget(content, stretch=1)

        self.top_bar = TopBar()
        content_layout.addWidget(self.top_bar)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet(f"background-color: {PALETTE.bg_primary};")
        content_layout.addWidget(self.stack, stretch=1)

        self._pages: dict[str, QWidget] = {}
        for page_cls in PAGE_CLASSES:
            page = page_cls()
            self._pages[page_cls.page_key] = page
            self.stack.addWidget(page)

        self._show_page(self._nav_vm.active_page)

    def _wire_signals(self) -> None:
        self.title_bar.minimize_requested.connect(self.showMinimized)
        self.title_bar.maximize_requested.connect(self._toggle_maximize)
        self.title_bar.close_requested.connect(self.close)

        self.sidebar.navigate_requested.connect(self._nav_vm.set_active_page)
        self.sidebar.toggle_requested.connect(self._nav_vm.set_sidebar_collapsed)
        self.sidebar.logout_requested.connect(self._on_logout_requested)

        self._nav_vm.active_page_changed.connect(self._show_page)

    def _restore_window_state(self) -> None:
        collapsed = bool(self._settings.value(SettingsKeys.SIDEBAR_COLLAPSED, False, type=bool))
        if collapsed:
            self.sidebar.set_collapsed(True)
            self._nav_vm.set_sidebar_collapsed(True)

    # -- Page switching ------------------------------------------------

    def _show_page(self, key: str) -> None:
        page = self._pages.get(key)
        if page is None:
            return
        self.stack.setCurrentWidget(page)
        self.sidebar.set_active(key)
        self.top_bar.set_page_title(page.page_title, page.page_subtitle)

    def _on_logout_requested(self) -> None:
        # Phase 1 has no authentication yet (see PRD Module 1, Phase 2).
        # Logging out simply closes the application for now.
        self.close()

    # -- Window controls -------------------------------------------------

    def _toggle_maximize(self) -> None:
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def closeEvent(self, event) -> None:  # noqa: N802 (Qt override)
        self._settings.setValue(SettingsKeys.SIDEBAR_COLLAPSED, self._nav_vm.sidebar_collapsed)
        self._settings.setValue(SettingsKeys.WINDOW_MAXIMIZED, self.isMaximized())
        if not self.isMaximized():
            self._settings.setValue(SettingsKeys.WINDOW_GEOMETRY, self.saveGeometry())
        database_manager.close()
        super().closeEvent(event)

    # -- Frameless edge-resize -------------------------------------------

    def _edge_at(self, pos: QPoint) -> Qt.Edges:
        edges = Qt.Edge(0)
        if self.isMaximized():
            return edges
        rect = self.rect()
        if pos.x() <= RESIZE_MARGIN:
            edges |= Qt.Edge.LeftEdge
        elif pos.x() >= rect.width() - RESIZE_MARGIN:
            edges |= Qt.Edge.RightEdge
        if pos.y() <= RESIZE_MARGIN:
            edges |= Qt.Edge.TopEdge
        elif pos.y() >= rect.height() - RESIZE_MARGIN:
            edges |= Qt.Edge.BottomEdge
        return edges

    def _cursor_for_edges(self, edges: Qt.Edges) -> Qt.CursorShape:
        horizontal = bool(edges & (Qt.Edge.LeftEdge | Qt.Edge.RightEdge))
        vertical = bool(edges & (Qt.Edge.TopEdge | Qt.Edge.BottomEdge))
        if (edges & Qt.Edge.LeftEdge and edges & Qt.Edge.TopEdge) or \
           (edges & Qt.Edge.RightEdge and edges & Qt.Edge.BottomEdge):
            return Qt.CursorShape.SizeFDiagCursor
        if (edges & Qt.Edge.RightEdge and edges & Qt.Edge.TopEdge) or \
           (edges & Qt.Edge.LeftEdge and edges & Qt.Edge.BottomEdge):
            return Qt.CursorShape.SizeBDiagCursor
        if horizontal:
            return Qt.CursorShape.SizeHorCursor
        if vertical:
            return Qt.CursorShape.SizeVerCursor
        return Qt.CursorShape.ArrowCursor

    def mousePressEvent(self, event) -> None:  # noqa: N802 (Qt override)
        if event.button() == Qt.MouseButton.LeftButton:
            edges = self._edge_at(event.position().toPoint())
            if edges:
                self._resize_edge = edges
                self.windowHandle().startSystemResize(edges)
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:  # noqa: N802 (Qt override)
        if not self._drag_active:
            edges = self._edge_at(event.position().toPoint())
            self.setCursor(self._cursor_for_edges(edges))
        super().mouseMoveEvent(event)


def _load_fonts() -> None:
    """Register bundled fonts (assets/fonts) if present; safe no-op otherwise.

    Phase 1 ships without bundled font files -- Inter/Poppins/Segoe UI are
    referenced by family name and Qt gracefully substitutes an installed
    system font when they aren't present. Dropping .ttf/.otf files into
    assets/fonts/ later will make this loader pick them up automatically.
    """
    from config import FONTS_DIR
    if not FONTS_DIR.exists():
        return
    for font_file in FONTS_DIR.glob("*.[ot]tf"):
        QFontDatabase.addApplicationFont(str(font_file))


def _load_stylesheet(app: QApplication) -> None:
    from config import STYLES_DIR
    qss_path = STYLES_DIR / "dark.qss"
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))


def main() -> int:
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    app.setOrganizationName(APP_INFO.organization)
    app.setApplicationName(APP_INFO.name)
    app.setApplicationVersion(APP_INFO.version)

    _load_fonts()
    _load_stylesheet(app)

    database_manager.initialize()

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
