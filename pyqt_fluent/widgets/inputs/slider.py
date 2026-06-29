from __future__ import annotations

from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QBrush, QPen, QMouseEvent
from PyQt6.QtWidgets import QWidget, QSizePolicy

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class Slider(ThemeAwareWidget, QWidget):
    qss_role = "fluent_slider"
    value_changed = pyqtSignal(float)

    def __init__(self, parent=None,
                 track_color=None, fill_color=None, thumb_color=None):
        super().__init__(parent)
        self.setFixedHeight(24)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._value = 0.0
        self._track = QColor()
        self._fill = QColor()
        self._thumb = QColor()
        self._custom_track = QColor(track_color) if track_color else None
        self._custom_fill = QColor(fill_color) if fill_color else None
        self._custom_thumb = QColor(thumb_color) if thumb_color else None
        self._hovered = False
        self._dragging = False
        self._init_theme_aware()

    def value(self):
        return self._value

    def set_value(self, v: float):
        self._value = max(0.0, min(1.0, v))
        self.update()
        self.value_changed.emit(self._value)

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        c = theme.component
        self._track = self._custom_track if self._custom_track else r.color(c.slider_track)
        self._fill = self._custom_fill if self._custom_fill else r.color(c.slider_fill)
        self._thumb = self._custom_thumb if self._custom_thumb else r.color(c.slider_thumb)
        self.update()

    def enterEvent(self, e):
        self._hovered = True
        self.update()

    def leaveEvent(self, e):
        self._hovered = False
        if not self._dragging:
            self.update()

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self._update_from_pos(e.position().x())

    def mouseMoveEvent(self, e: QMouseEvent):
        if self._dragging:
            self._update_from_pos(e.position().x())

    def mouseReleaseEvent(self, e: QMouseEvent):
        self._dragging = False
        self.update()

    def _update_from_pos(self, x: float):
        w = self.width() - 24
        if w <= 0:
            return
        v = max(0.0, min(1.0, (x - 12) / w))
        self.set_value(v)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        h = self.height()
        track_h = 4
        track_y = (h - track_h) / 2

        track_rect = QRectF(12, track_y, self.width() - 24, track_h)
        track_path = QPainterPath()
        track_path.addRoundedRect(track_rect, 2, 2)
        painter.fillPath(track_path, QBrush(self._track))

        fill_w = track_rect.width() * self._value
        if fill_w > 0:
            fill_rect = QRectF(track_rect.x(), track_rect.y(), fill_w, track_h)
            fill_path = QPainterPath()
            fill_path.addRoundedRect(fill_rect, 2, 2)
            painter.fillPath(fill_path, QBrush(self._fill))

        thumb_x = track_rect.x() + track_rect.width() * self._value - 8
        thumb_rect = QRectF(thumb_x, (h - 16) / 2, 16, 16)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self._thumb))
        painter.drawEllipse(thumb_rect)

        if self._hovered or self._dragging:
            ring_rect = QRectF(thumb_x - 4, (h - 24) / 2, 24, 24)
            pen = QPen(self._fill, 2)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(ring_rect)
