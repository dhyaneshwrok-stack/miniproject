"""
PulseMind - Base ViewModel
=============================

Root of the MVVM view-model hierarchy. A QObject subclass so every
view-model can expose Qt signals that views bind to, without any
view-model importing widget classes directly (keeping presentation
logic testable and UI-framework-agnostic where possible).
"""

from __future__ import annotations

from PySide6.QtCore import QObject


class BaseViewModel(QObject):
    """Marker base class for all view-models in the application.

    Phase 1 view-models hold only placeholder/static state since no
    services or database queries are wired up yet. Future phases will
    inject `services/` instances here and replace static values with
    live data, without views needing to change how they consume signals.
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
