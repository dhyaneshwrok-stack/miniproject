# PulseMind — Phase 1: UI Architecture & Application Foundation

Smart ECG Signal Analysis & Report Generation System
**Phase 1 scope:** architecture, navigation, reusable components, and the
premium dark medical UI foundation only. No ECG processing, signal
analysis, report generation, or patient CRUD is implemented yet — see
`config.py::FeatureFlags` and the roadmap on the **About** page.

---

## 1. Requirements

- Windows 10/11 (developed to also run cross-platform for testing)
- Python 3.13+ (3.10+ will also work for Phase 1)

## 2. Setup

```bash
cd PulseMind
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux (for dev/testing only)

pip install -r requirements.txt
```

Phase 1 only requires **PySide6** — the rest of `requirements.txt` is
commented out and reserved for later phases (PyQtGraph, pandas,
NumPy/SciPy, ReportLab, Pillow, PyInstaller), matching the PRD's
technology stack.

## 3. Run

```bash
python main.py
```

A frameless, rounded, dark medical-themed window opens at 1600×1000
(minimum 1400×900), with a collapsible sidebar, top bar, and seven
navigation pages: Dashboard, Patients, ECG Analysis, Reports, History,
Settings, About.

## 4. Project Structure

```
PulseMind/
├── main.py                  # App bootstrap + frameless MainWindow
├── config.py                 # Static config: paths, window/sidebar sizing,
│                              # nav items, settings keys, feature flags
├── requirements.txt
│
├── assets/
│   ├── icons/                # Reserved for bundled icon assets (icons are
│   │                          # currently vector-drawn in code, see utils/icons.py)
│   ├── images/
│   └── fonts/                # Drop .ttf/.otf files here to bundle Inter/Poppins
│
├── database/
│   └── database.py           # SQLite connection manager (connect + init only)
│
├── styles/
│   ├── theme.py               # Single source of truth: palette, spacing,
│   │                           # radii, typography, motion durations
│   └── dark.qss                # Global QSS for native Qt widgets (scrollbars,
│                                # tooltips, etc.)
│
├── models/                    # Reserved for Phase 2 (Patient, Report, User)
├── viewmodels/
│   ├── base_viewmodel.py
│   └── navigation_viewmodel.py  # Active page + sidebar collapsed state
│
├── views/                      # One placeholder page per module
│   ├── base_page.py             # Shared scrollable page shell
│   ├── dashboard.py
│   ├── patients.py
│   ├── analysis.py
│   ├── reports.py
│   ├── history.py
│   ├── settings.py
│   └── about.py
│
├── widgets/                     # Reusable component library
│   ├── buttons.py                # PrimaryButton, SecondaryButton, DangerButton, IconButton
│   ├── cards.py                   # StatCard, InfoCard, EmptyStateCard
│   ├── tables.py                   # StyledTableWidget
│   ├── dialogs.py                   # ConfirmationDialog, MessageDialog, LoadingDialog
│   ├── badges.py                     # StatusBadge
│   ├── inputs.py                      # SearchBox, Dropdown, DatePicker
│   ├── sidebar.py                      # Collapsible animated navigation
│   ├── topbar.py                        # Page title, search, notifications, avatar, date
│   └── titlebar.py                       # Custom frameless title bar (drag/min/max/close)
│
├── services/                    # Reserved for Phase 3+ (dataset loading,
│                                 # signal processing, report generation)
└── utils/
    ├── icons.py                  # Vector line-icon renderer (no image assets needed)
    └── animations.py              # Reusable width/opacity animation helpers
```

## 5. Architecture Notes

- **Pattern:** MVVM-leaning. `viewmodels/` currently owns only
  navigation/UI state (which page is active, sidebar collapsed or not)
  since there's no business data yet. Future phases add
  `PatientsViewModel`, `AnalysisViewModel`, etc., backed by `services/`.
- **Theming:** every color, spacing value, radius, and font comes from
  `styles/theme.py`. Nothing is hardcoded in widgets or views — this is
  what makes future re-theming (e.g. a light mode) a one-file change.
- **Icons:** rendered on demand as crisp vector line-art
  (`utils/icons.py`) rather than shipped as image files, so the app has
  zero missing-asset risk. Swappable later for a bundled icon set
  without touching call sites.
- **Database:** `database/database.py` opens a WAL-mode SQLite
  connection and guarantees the file/folder exist. No tables are
  created in Phase 1, per scope.
- **Frameless window:** the real `QMainWindow` is fully transparent; a
  rounded `QFrame` (`self.container`) with a soft drop shadow draws the
  visible surface, with `TitleBar` handling dragging and
  `startSystemResize()` handling edge-resizing.

## 6. What's Intentionally Not Implemented Yet

Per Phase 1 scope: authentication, patient CRUD, dataset loading, ECG
waveform rendering, signal processing, parameter calculation, PDF
report generation, report history persistence, and database
backup/restore/export are all UI shells only. Buttons for these
actions are visibly disabled with a tooltip explaining which future
phase unlocks them.
