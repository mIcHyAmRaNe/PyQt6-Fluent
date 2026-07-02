from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt, QTimer
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QSizePolicy, QWidget

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class ProgressRing(ThemeAwareWidget, QWidget):
    """Circular indeterminate/eterminate progress indicator matching FluProgressRing.qml."""

    def __init__(self, parent=None, stroke_width=6, value=0.0,
                 indeterminate=True, duration=2000):
        super().__init__(parent)
        self._stroke_width = stroke_width
        self._value = max(0.0, min(1.0, value))
        self._indeterminate = indeterminate
        self._duration = duration
        self._color = QColor()
        self._bg_color = QColor()
        self._start_angle = 0.0
        self._sweep_angle = 0.0
        self._progress_visible = False
        self._custom_color = None

        self.setFixedSize(56, 56)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self._indeterminate_timer = QTimer(self)
        self._indeterminate_timer.setInterval(16)
        self._indeterminate_timer.timeout.connect(self._tick_indeterminate)

        self._phase = 0
        self._phase_time = 0
        self._phase_duration = duration // 2

        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._color = self._custom_color if self._custom_color else r.color("semantic.accent")
        self._bg_color = r.color("palette.slider_track")
        self.update()

    def setValue(self, v: float):
        self._value = max(0.0, min(1.0, v))
        self._indeterminate = False
        self._indeterminate_timer.stop()
        self.update()

    def setIndeterminate(self, on: bool):
        self._indeterminate = on
        if on:
            self._phase = 0
            self._phase_time = 0
            self._start_angle = 0.0
            self._sweep_angle = 0.0
            self._indeterminate_timer.start()
        else:
            self._indeterminate_timer.stop()
        self.update()

    def _tick_indeterminate(self):
        self._phase_time += 16
        t = self._phase_time / self._phase_duration
        if t >= 1.0:
            t = 1.0
            self._phase = 1 - self._phase
            self._phase_time = 0

        if self._phase == 0:
            self._start_angle = t * 450.0
            self._sweep_angle = min(t * 180.0, 180.0)
        else:
            self._start_angle = 450.0 + t * 630.0
            self._sweep_angle = 180.0 * (1.0 - t)

        self.update()

    def showEvent(self, e):
        super().showEvent(e)
        if self._indeterminate:
            self._indeterminate_timer.start()

    def hideEvent(self, e):
        super().hideEvent(e)
        self._indeterminate_timer.stop()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2
        radius = (min(w, h) - self._stroke_width) / 2

        # Background circle
        pen = QPen(self._bg_color, self._stroke_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawEllipse(QRectF(cx - radius, cy - radius, radius * 2, radius * 2))

        # Progress arc
        pen.setColor(self._color)
        painter.setPen(pen)

        if self._indeterminate:
            start = (self._start_angle - 90) * 16
            sweep = self._sweep_angle * 16
            painter.drawArc(QRectF(cx - radius, cy - radius, radius * 2, radius * 2),
                            int(start), int(sweep))
        elif self._value > 0:
            span = self._value * 360 * 16
            painter.drawArc(QRectF(cx - radius, cy - radius, radius * 2, radius * 2),
                            -90 * 16, int(span))

        painter.end()
