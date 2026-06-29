"""Ripple effect — Material-like click ripple animation."""

from PyQt6.QtCore import QObject, QPointF, QPropertyAnimation, QRectF, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QRadialGradient
from PyQt6.QtWidgets import QWidget


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
        self._anim.setDuration(400)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)

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

    def paint(self, painter: QPainter, rect: QRectF) -> None:
        if self._radius <= 0.0:
            return
        g = QRadialGradient(self._origin, self._radius)
        g.setColorAt(0.0, self._color)
        g.setColorAt(1.0, QColor(0, 0, 0, 0))
        painter.save()
        painter.setClipRect(rect)
        painter.fillRect(rect, g)
        painter.restore()
