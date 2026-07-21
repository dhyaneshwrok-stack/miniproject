"""
PulseMind - Application Configuration
=======================================

Centralized, static configuration for the application. Nothing in this
module should depend on Qt so it can be imported anywhere (services,
database layer, widgets) without creating import cycles.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

ROOT_DIR: Path = Path(__file__).resolve().parent
ASSETS_DIR: Path = ROOT_DIR / "assets"
ICONS_DIR: Path = ASSETS_DIR / "icons"
IMAGES_DIR: Path = ASSETS_DIR / "images"
FONTS_DIR: Path = ASSETS_DIR / "fonts"
DATABASE_DIR: Path = ROOT_DIR / "database"
DATABASE_FILE: Path = DATABASE_DIR / "database.db"
STYLES_DIR: Path = ROOT_DIR / "styles"


# --------------------------------------------------------------------------
# Application metadata
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class AppInfo:
    """Static, immutable metadata describing the application."""

    name: str = "PulseMind"
    tagline: str = "Smart ECG Signal Analysis & Report Generation System"
    version: str = "0.1.0 (Phase 1 - UI Foundation)"
    organization: str = "PulseMind"
    college: str = "Academic Mini Project"


APP_INFO = AppInfo()


# --------------------------------------------------------------------------
# Window configuration
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class WindowConfig:
    """Constraints and defaults for the main application window."""

    min_width: int = 1400
    min_height: int = 900
    default_width: int = 1600
    default_height: int = 950
    corner_radius: int = 16
    titlebar_height: int = 56
    resize_margin: int = 6


WINDOW_CONFIG = WindowConfig()


# --------------------------------------------------------------------------
# Sidebar configuration
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class SidebarConfig:
    """Sizing and animation timing for the collapsible sidebar."""

    expanded_width: int = 264
    collapsed_width: int = 84
    animation_duration_ms: int = 220


SIDEBAR_CONFIG = SidebarConfig()


# --------------------------------------------------------------------------
# Misc feature flags (reserved for future phases)
# --------------------------------------------------------------------------

class FeatureFlags:
    """Feature flags reserved for future development phases.

    Phase 1 intentionally ships with all business-logic features disabled.
    These flags exist so future phases can toggle functionality without
    restructuring the navigation or view layer.
    """

    ECG_PROCESSING_ENABLED: bool = False
    REPORT_GENERATION_ENABLED: bool = False
    PATIENT_CRUD_ENABLED: bool = False


# --------------------------------------------------------------------------
# Navigation
# --------------------------------------------------------------------------

NAV_ITEMS: list[dict] = [
    {"key": "dashboard", "label": "Dashboard", "icon": "dashboard"},
    {"key": "patients", "label": "Patients", "icon": "patients"},
    {"key": "analysis", "label": "ECG Analysis", "icon": "ecg"},
    {"key": "reports", "label": "Reports", "icon": "reports"},
    {"key": "history", "label": "History", "icon": "history"},
    {"key": "settings", "label": "Settings", "icon": "settings"},
    {"key": "about", "label": "About", "icon": "about"},
]


# --------------------------------------------------------------------------
# QSettings keys (persisted preferences)
# --------------------------------------------------------------------------

class SettingsKeys:
    """String keys used with QSettings for lightweight preference storage."""

    THEME: str = "appearance/theme"
    SIDEBAR_COLLAPSED: str = "ui/sidebar_collapsed"
    WINDOW_GEOMETRY: str = "window/geometry"
    WINDOW_MAXIMIZED: str = "window/maximized"
