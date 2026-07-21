"""
PulseMind - Animation Helpers
================================

Small, reusable Qt animation builders so every widget (sidebar, pages,
cards, dialogs) produces smooth, consistent motion instead of each
hand-rolling its own QPropertyAnimation.
"""

from __future__ import annotations

from PySide6.QtCore import (
    QAbstractAnimation, QEasingCurve, QPropertyAnimation, QVariantAnimation,
)
from PySide6.QtWidgets import QGraphicsOpacityEffect, QWidget

from styles.theme import MOTION


def animate_width(widget: QWidget, start: int, end: int,
                   duration: int = MOTION.base,
                   easing: QEasingCurve.Type = QEasingCurve.Type.OutCubic
                   ) -> QPropertyAnimation:
    """Animate a widget's fixed width (used for sidebar collapse/expand)."""
    animation = QPropertyAnimation(widget, b"minimumWidth", widget)
    animation.setStartValue(start)
    animation.setEndValue(end)
    animation.setDuration(duration)
    animation.setEasingCurve(easing)

    max_animation = QPropertyAnimation(widget, b"maximumWidth", widget)
    max_animation.setStartValue(start)
    max_animation.setEndValue(end)
    max_animation.setDuration(duration)
    max_animation.setEasingCurve(easing)
    max_animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
    return animation


def fade_widget(widget: QWidget, start: float = 0.0, end: float = 1.0,
                 duration: int = MOTION.base) -> QPropertyAnimation:
    """Fade a widget's opacity in or out; returns the running animation."""
    effect = widget.graphicsEffect()
    if not isinstance(effect, QGraphicsOpacityEffect):
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b"opacity", widget)
    animation.setStartValue(start)
    animation.setEndValue(end)
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.Type.OutCubic)
    animation.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
    return animation
