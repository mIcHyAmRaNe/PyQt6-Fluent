from __future__ import annotations

from PyQt6.QtCore import Qt, QRectF, QPropertyAnimation, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QWidget, QSizePolicy

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class Spinner(ThemeAwareWidget, QWidget):
    qss_role = "fluent_spinner"

    def __init__(self, size=20, parent=None, color=None):
        super().__init__(parent)
        self._size = size
        self.setFixedSize(size, size)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._color = QColor()
        self._custom_color = QColor(color) if color else None
        self._angle = 0.0

        self._ani = QPropertyAnimation(self, b"angle", self)
        self._ani.setDuration(1000)
        self._ani.setStartValue(0.0)
        self._ani.setEndValue(360.0)
        self._ani.setLoopCount(-1)

        self._init_theme_aware()

    def _get_angle(self) -> float:
        return self._angle

    def _set_angle(self, v: float) -> None:
        self._angle = v
        self.update()

    angle = pyqtProperty(float, _get_angle, _set_angle)

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._color = self._custom_color if self._custom_color else r.color("semantic.accent")
        self.update()

    def showEvent(self, e):
        super().showEvent(e)
        self._ani.start()

    def hideEvent(self, e):
        self._ani.stop()
        super().hideEvent(e)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect()).adjusted(2, 2, -2, -2)
        pen = QPen(self._color, 3)
        pen.setCosmetic(True)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawArc(rect, int(-self._angle * 16), int(120 * 16))
