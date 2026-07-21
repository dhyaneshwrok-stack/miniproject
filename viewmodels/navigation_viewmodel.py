"""
PulseMind - Navigation ViewModel
===================================

Owns the single piece of shared UI state that isn't specific to any
one page: which page is currently active, and whether the sidebar is
collapsed. The main window binds the sidebar and top bar to this
view-model instead of having them talk to each other directly.
"""

from __future__ import annotations

from PySide6.QtCore import Signal

from config import NAV_ITEMS
from viewmodels.base_viewmodel import BaseViewModel


class NavigationViewModel(BaseViewModel):
    """Tracks the active page key and sidebar collapsed state."""

    active_page_changed = Signal(str)
    sidebar_collapsed_changed = Signal(bool)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._page_keys = {item["key"] for item in NAV_ITEMS}
        self._active_page: str = NAV_ITEMS[0]["key"]
        self._sidebar_collapsed: bool = False

    @property
    def active_page(self) -> str:
        return self._active_page

    @property
    def sidebar_collapsed(self) -> bool:
        return self._sidebar_collapsed

    def set_active_page(self, key: str) -> None:
        if key not in self._page_keys or key == self._active_page:
            return
        self._active_page = key
        self.active_page_changed.emit(key)

    def set_sidebar_collapsed(self, collapsed: bool) -> None:
        if collapsed == self._sidebar_collapsed:
            return
        self._sidebar_collapsed = collapsed
        self.sidebar_collapsed_changed.emit(collapsed)
