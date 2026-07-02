"""Shared animation helpers — WinUI 3 easing curves and common utilities."""

from __future__ import annotations

from PyQt6.QtCore import QEasingCurve, QPointF


def winui_easing(duration: int = 83) -> QEasingCurve:
    """WinUI 3 FastOutSlowIn — cubic-bezier(0.1, 0.9, 0.2, 1.0)."""
    e = QEasingCurve(QEasingCurve.Type.BezierSpline)
    e.addCubicBezierSegment(QPointF(0.1, 0.9), QPointF(0.2, 1.0), QPointF(1.0, 1.0))
    return e


WINUI_FAST_OUT_SLOW_IN = winui_easing
