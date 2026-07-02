from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt, pyqtSignal
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QFontMetrics,
    QMouseEvent,
    QPainter,
    QPainterPath,
)
from PyQt6.QtWidgets import QSizePolicy, QWidget

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class Slider(ThemeAwareWidget, QWidget):
    qss_role = "fluent_slider"
    value_changed = pyqtSignal(float)

    def __init__(self, parent=None,
                 track_color=None, fill_color=None, thumb_color=None):
        super().__init__(parent)
        self.setFixedHeight(28)
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
        self._thumb_scale = 1.0
        self.setMouseTracking(True)
        self._init_theme_aware()

    def value(self):
        return self._value

    def set_value(self, v: float):
        self._value = max(0.0, min(1.0, v))
        self.update()
        self.value_changed.emit(self._value)

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._track = self._custom_track if self._custom_track else r.color("palette.slider_track")
        self._fill = self._custom_fill if self._custom_fill else r.color("semantic.accent")
        self._thumb = self._custom_thumb if self._custom_thumb else r.color("palette.slider_handle")
        self._is_dark = theme.is_dark
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
        track_h = 6
        track_y = (h - track_h) / 2
        track_r = 3.0

        # Background track
        track_rect = QRectF(12, track_y, self.width() - 24, track_h)
        track_path = QPainterPath()
        track_path.addRoundedRect(track_rect, track_r, track_r)
        painter.fillPath(track_path, QBrush(self._track))

        # Filled portion
        fill_w = track_rect.width() * self._value
        if fill_w > 0:
            fill_rect = QRectF(track_rect.x(), track_rect.y(), fill_w, track_h)
            fill_path = QPainterPath()
            fill_path.addRoundedRect(fill_rect, track_r, track_r)
            painter.fillPath(fill_path, QBrush(self._fill))

        # Thumb (20x20 circle with high-performance shadow)
        thumb_size = 20
        thumb_x = track_rect.x() + track_rect.width() * self._value - thumb_size / 2
        thumb_rect = QRectF(thumb_x, (h - thumb_size) / 2, thumb_size, thumb_size)

        # High-performance shadow (FluShadow style: stacked borders)
        shadow_color = QColor(153, 153, 153) if not self._is_dark else QColor(0, 0, 0)
        for i in range(5):
            opacity = 0.01 * (5 - i + 1)
            shadow_color_i = QColor(shadow_color)
            shadow_color_i.setAlphaF(opacity)
            margin = -i
            sr = thumb_rect.adjusted(margin, margin, -margin, -margin)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(shadow_color_i))
            painter.drawEllipse(sr)

        # Thumb background
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self._thumb))
        painter.drawEllipse(thumb_rect)

        # Accent dot inside thumb (10px, scales on hover/press)
        dot_size = 10
        if self._dragging:
            dot_size = 9
        elif self._hovered:
            dot_size = 12

        dot_rect = QRectF(
            thumb_x + (thumb_size - dot_size) / 2,
            (h - dot_size) / 2,
            dot_size, dot_size,
        )
        painter.setBrush(QBrush(self._fill))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(dot_rect)

        # Tooltip on hover/press
        if self._hovered or self._dragging:
            pct = int(self._value * 100)
            text = f"{pct}%"
            font = QFont("Segoe UI Variable", 10)
            painter.setFont(font)
            fm = QFontMetrics(font)
            tw = fm.horizontalAdvance(text)
            th = fm.height()
            tooltip_x = thumb_x + thumb_size / 2 - tw / 2
            tooltip_y = thumb_rect.y() - th - 8
            tooltip_rect = QRectF(tooltip_x - 6, tooltip_y - 4, tw + 12, th + 8)
            tooltip_bg = QColor(45, 45, 45) if not self._is_dark else QColor(252, 252, 252)
            tooltip_fg = QColor(255, 255, 255) if not self._is_dark else QColor(0, 0, 0)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(tooltip_bg))
            painter.drawRoundedRect(tooltip_rect, 4, 4)
            painter.setPen(tooltip_fg)
            painter.drawText(tooltip_rect, Qt.AlignmentFlag.AlignCenter, text)

        painter.end()
