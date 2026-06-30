"""Ripple effect — Material-like click ripple animation."""

from PyQt6.QtCore import QEasingCurve, QObject, QPointF, QPropertyAnimation, QRectF, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QRadialGradient
from PyQt6.QtWidgets import QWidget


def _winui_easing() -> QEasingCurve:
    """WinUI 3 FastOutSlowIn — cubic-bezier(0.1, 0.9, 0.2, 1.0)."""
    e = QEasingCurve(QEasingCurve.Type.BezierSpline)
    e.addCubicBezierSegment(QPointF(0.1, 0.9), QPointF(0.2, 1.0), QPointF(1.0, 1.0))
    return e


class RippleEffect(QObject):
    """Click ripple animation helper.

    Usage in paintEvent:
        self._ripple.paint(painter, self.rect())
    """

    def __init__(self, parent: QWidget, color: QColor = QColor(255, 255, 255, 80)):
        super().__init__(parent)
        self._parent = parent
        self._color = color
        self._radius = 0.0
        self._origin = QPointF()
        self._anim = QPropertyAnimation(self, b"radius", self)
        self._anim.setDuration(250)
        self._anim.setEasingCurve(_winui_easing())
        self._anim.finished.connect(self._on_ripple_finished)

    def _get_radius(self) -> float:
        return self._radius

    def _set_radius(self, r: float) -> None:
        self._radius = r
        self._parent.update()

    radius = pyqtProperty(float, _get_radius, _set_radius)

    def start(self, pos: QPointF) -> None:
        self._origin = pos
        max_dim = max(self._parent.width(), self._parent.height())
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(float(max_dim) * 1.5)
        self._anim.start()

    def _on_ripple_finished(self) -> None:
        self._radius = 0.0
        self._parent.update()

    def paint(self, painter: QPainter, rect: QRectF, radius: float = 0) -> None:
        if self._radius <= 0.0:
            return
        g = QRadialGradient(self._origin, self._radius)
        g.setColorAt(0.0, self._color)
        g.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.save()
        if radius > 0:
            path = QPainterPath()
            path.addRoundedRect(rect, radius, radius)
            painter.setClipPath(path)
        else:
            painter.setClipRect(rect)
        painter.fillRect(rect, g)
        painter.restore()
