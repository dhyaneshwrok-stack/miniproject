"""
PulseMind - Icon Provider
============================

Phase 1 ships without a bundled icon font or raster icon set. Instead,
icons are drawn on demand as crisp vector QIcons using simple QPainterPath
line-art. This keeps the app fully self-contained (no missing-asset risk)
while still looking custom-designed rather than "default Qt".

Future phases can swap this module's implementation for a bundled SVG
icon set (e.g. Phosphor/Lucide) without changing any call sites, since
everything is accessed through :func:`icon`.
"""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QIcon, QPainter, QPainterPath, QPen, QPixmap

from styles.theme import PALETTE, qcolor

# --------------------------------------------------------------------------
# Path builders -- each returns a QPainterPath drawn in a 24x24 box.
# --------------------------------------------------------------------------


def _path_dashboard(p: QPainterPath) -> None:
    p.addRoundedRect(QRectF(3, 3, 8, 8), 2, 2)
    p.addRoundedRect(QRectF(13, 3, 8, 5), 2, 2)
    p.addRoundedRect(QRectF(13, 10, 8, 11), 2, 2)
    p.addRoundedRect(QRectF(3, 13, 8, 8), 2, 2)


def _path_patients(p: QPainterPath) -> None:
    p.addEllipse(QRectF(8, 3, 8, 8))
    p.moveTo(4, 21)
    p.cubicTo(4, 15, 20, 15, 20, 21)


def _path_ecg(p: QPainterPath) -> None:
    p.moveTo(2, 13)
    p.lineTo(7, 13)
    p.lineTo(9, 6)
    p.lineTo(12, 19)
    p.lineTo(14, 10)
    p.lineTo(16, 13)
    p.lineTo(22, 13)


def _path_reports(p: QPainterPath) -> None:
    p.addRoundedRect(QRectF(5, 2, 14, 20), 2, 2)
    for y in (8, 12, 16):
        p.moveTo(8, y)
        p.lineTo(16, y)


def _path_history(p: QPainterPath) -> None:
    p.addEllipse(QRectF(3, 3, 18, 18))
    p.moveTo(12, 7)
    p.lineTo(12, 12)
    p.lineTo(16, 14)


def _path_settings(p: QPainterPath) -> None:
    p.addEllipse(QRectF(8, 8, 8, 8))
    for i in range(8):
        import math
        angle = i * (360 / 8)
        rad = math.radians(angle)
        cx, cy, r1, r2 = 12, 12, 9, 11
        x1, y1 = cx + r1 * math.cos(rad), cy + r1 * math.sin(rad)
        x2, y2 = cx + r2 * math.cos(rad), cy + r2 * math.sin(rad)
        p.moveTo(x1, y1)
        p.lineTo(x2, y2)


def _path_about(p: QPainterPath) -> None:
    p.addEllipse(QRectF(3, 3, 18, 18))
    p.addEllipse(QRectF(11, 7, 2, 2))
    p.moveTo(12, 11)
    p.lineTo(12, 17)


def _path_logout(p: QPainterPath) -> None:
    p.addRoundedRect(QRectF(4, 4, 9, 16), 2, 2)
    p.moveTo(11, 12)
    p.lineTo(21, 12)
    p.moveTo(17, 8)
    p.lineTo(21, 12)
    p.lineTo(17, 16)


def _path_search(p: QPainterPath) -> None:
    p.addEllipse(QRectF(3, 3, 12, 12))
    p.moveTo(13, 13)
    p.lineTo(20, 20)


def _path_bell(p: QPainterPath) -> None:
    p.moveTo(6, 16)
    p.cubicTo(6, 10, 6, 5, 12, 5)
    p.cubicTo(18, 5, 18, 10, 18, 16)
    p.lineTo(20, 19)
    p.lineTo(4, 19)
    p.closeSubpath()
    p.addEllipse(QRectF(10, 20, 4, 2))


def _path_chevron_left(p: QPainterPath) -> None:
    p.moveTo(15, 4)
    p.lineTo(8, 12)
    p.lineTo(15, 20)


def _path_chevron_right(p: QPainterPath) -> None:
    p.moveTo(9, 4)
    p.lineTo(16, 12)
    p.lineTo(9, 20)


def _path_chevron_down(p: QPainterPath) -> None:
    p.moveTo(4, 9)
    p.lineTo(12, 16)
    p.lineTo(20, 9)


def _path_calendar(p: QPainterPath) -> None:
    p.addRoundedRect(QRectF(3, 5, 18, 16), 3, 3)
    p.moveTo(3, 10)
    p.lineTo(21, 10)
    p.moveTo(8, 2)
    p.lineTo(8, 6)
    p.moveTo(16, 2)
    p.lineTo(16, 6)


def _path_plus(p: QPainterPath) -> None:
    p.moveTo(12, 4)
    p.lineTo(12, 20)
    p.moveTo(4, 12)
    p.lineTo(20, 12)


def _path_close(p: QPainterPath) -> None:
    p.moveTo(5, 5)
    p.lineTo(19, 19)
    p.moveTo(19, 5)
    p.lineTo(5, 19)


def _path_minimize(p: QPainterPath) -> None:
    p.moveTo(5, 12)
    p.lineTo(19, 12)


def _path_maximize(p: QPainterPath) -> None:
    p.addRect(QRectF(5, 5, 14, 14))


def _path_user(p: QPainterPath) -> None:
    p.addEllipse(QRectF(7, 3, 10, 10))
    p.moveTo(3, 21)
    p.cubicTo(3, 15, 21, 15, 21, 21)


def _path_warning(p: QPainterPath) -> None:
    p.moveTo(12, 3)
    p.lineTo(22, 20)
    p.lineTo(2, 20)
    p.closeSubpath()
    p.moveTo(12, 9)
    p.lineTo(12, 14)
    p.addEllipse(QRectF(11.2, 16, 1.6, 1.6))


def _path_inbox(p: QPainterPath) -> None:
    p.addRoundedRect(QRectF(3, 7, 18, 13), 2, 2)
    p.moveTo(3, 13)
    p.lineTo(9, 13)
    p.lineTo(10.5, 16)
    p.lineTo(13.5, 16)
    p.lineTo(15, 13)
    p.lineTo(21, 13)


_PATH_BUILDERS = {
    "dashboard": _path_dashboard,
    "patients": _path_patients,
    "ecg": _path_ecg,
    "reports": _path_reports,
    "history": _path_history,
    "settings": _path_settings,
    "about": _path_about,
    "logout": _path_logout,
    "search": _path_search,
    "bell": _path_bell,
    "chevron_left": _path_chevron_left,
    "chevron_right": _path_chevron_right,
    "chevron_down": _path_chevron_down,
    "calendar": _path_calendar,
    "plus": _path_plus,
    "close": _path_close,
    "minimize": _path_minimize,
    "maximize": _path_maximize,
    "user": _path_user,
    "warning": _path_warning,
    "inbox": _path_inbox,
}


def render_icon(name: str, color: str = PALETTE.text_secondary,
                 size: int = 22, stroke_width: float = 1.6) -> QIcon:
    """Render a named icon as a QIcon using vector line-art.

    Args:
        name: Icon key, one of ``_PATH_BUILDERS``.
        color: Hex/CSS color string for the stroke.
        size: Pixel size of the square icon.
        stroke_width: Line thickness in the 24x24 design grid.

    Returns:
        A QIcon rendered at the requested size (2x pixmap for crispness).
    """
    builder = _PATH_BUILDERS.get(name)
    if builder is None:
        builder = _path_about  # graceful fallback, never crash on a typo

    scale = 2
    pixmap = QPixmap(size * scale, size * scale)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.scale((size * scale) / 24, (size * scale) / 24)

    pen = QPen(qcolor(color))
    pen.setWidthF(stroke_width)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    path = QPainterPath()
    builder(path)
    painter.drawPath(path)
    painter.end()

    return QIcon(pixmap)


def icon(name: str, color: str = PALETTE.text_secondary, size: int = 22) -> QIcon:
    """Public convenience accessor -- see :func:`render_icon`."""
    return render_icon(name, color=color, size=size)
