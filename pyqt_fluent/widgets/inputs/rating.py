from __future__ import annotations

from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QBrush, QPen, QMouseEvent
from PyQt6.QtWidgets import QWidget, QSizePolicy

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class Rating(ThemeAwareWidget, QWidget):
    qss_role = "fluent_rating"
    value_changed = pyqtSignal(float)

    def __init__(self, max_stars=5, parent=None,
                 fill_color=None, empty_color=None):
        super().__init__(parent)
        self.setFixedHeight(24)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self._max = max_stars
        self._value = 0
        self._accent = QColor()
        self._subtle = QColor()
        self._custom_fill = QColor(fill_color) if fill_color else None
        self._custom_empty = QColor(empty_color) if empty_color else None
        self._init_theme_aware()

    def value(self):
        return self._value

    def set_value(self, v: int):
        self._value = max(0, min(self._max, v))
        self.update()
        self.value_changed.emit(float(self._value))

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._accent = self._custom_fill if self._custom_fill else r.color("semantic.accent")
        self._subtle = self._custom_empty if self._custom_empty else r.color("semantic.subtle_fill")
        self.update()

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.MouseButton.LeftButton:
            star = int(e.position().x() / 24)
            self.set_value(star + 1)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        for i in range(self._max):
            x = i * 24 + 2
            rect = QRectF(x, 2, 20, 20)
            filled = i < self._value
            color = self._accent if filled else self._subtle
            painter.setPen(QPen(color, 1))
            painter.setBrush(QBrush(color))
            self._draw_star(painter, rect)

    def _draw_star(self, painter: QPainter, rect: QRectF):
        cx, cy = rect.center().x(), rect.center().y()
        r = rect.width() / 2
        path = QPainterPath()
        for i in range(5):
            angle = -90 + i * 72
            px = cx + r * __import__("math").cos(__import__("math").radians(angle))
            py = cy + r * __import__("math").sin(__import__("math").radians(angle))
            if i == 0:
                path.moveTo(px, py)
            else:
                path.lineTo(px, py)
            angle2 = -90 + i * 72 + 36
            px2 = cx + r * 0.4 * __import__("math").cos(__import__("math").radians(angle2))
            py2 = cy + r * 0.4 * __import__("math").sin(__import__("math").radians(angle2))
            path.lineTo(px2, py2)
        path.closeSubpath()
        painter.drawPath(path)
