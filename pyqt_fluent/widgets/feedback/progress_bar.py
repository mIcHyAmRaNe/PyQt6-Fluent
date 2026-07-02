from __future__ import annotations

from PyQt6.QtCore import QPropertyAnimation, QRectF, pyqtProperty
from PyQt6.QtGui import QBrush, QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import QSizePolicy, QWidget

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class ProgressBar(ThemeAwareWidget, QWidget):
    qss_role = "fluent_progress"

    def __init__(self, parent=None,
                 rail_color=None, fill_color=None):
        super().__init__(parent)
        self.setFixedHeight(6)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._value = 0.0
        self._rail = QColor()
        self._fill = QColor()
        self._custom_rail = QColor(rail_color) if rail_color else None
        self._custom_fill = QColor(fill_color) if fill_color else None
        self._indeterminate = False
        self._indet_pos = 0.0

        self._indet_ani = QPropertyAnimation(self, b"indet_pos", self)
        self._indet_ani.setDuration(888)
        self._indet_ani.setStartValue(-0.3)
        self._indet_ani.setEndValue(1.3)
        self._indet_ani.setLoopCount(-1)

        self._init_theme_aware()

    def _get_indet(self) -> float:
        return self._indet_pos

    def _set_indet(self, v: float) -> None:
        self._indet_pos = v
        self.update()

    indet_pos = pyqtProperty(float, _get_indet, _set_indet)

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        if self._custom_rail:
            self._rail = self._custom_rail
        else:
            self._rail = r.color("component.progressbar_rail")
        self._fill = self._custom_fill if self._custom_fill else r.color("component.progressbar_fill")
        self.update()

    def set_value(self, v: float):
        self._value = max(0.0, min(1.0, v))
        self._indeterminate = False
        self._indet_ani.stop()
        self.update()

    def set_indeterminate(self, ind: bool):
        self._indeterminate = ind
        if ind and self.isVisible():
            self._indet_ani.start()
        else:
            self._indet_ani.stop()
        self.update()

    def showEvent(self, e):
        super().showEvent(e)
        if self._indeterminate:
            self._indet_ani.start()

    def hideEvent(self, e):
        self._indet_ani.stop()
        super().hideEvent(e)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect())
        r = 3.0
        path = QPainterPath()
        path.addRoundedRect(rect, r, r)
        painter.fillPath(path, QBrush(self._rail))

        if self._indeterminate:
            w = rect.width() * 0.5
            x = self._indet_pos * rect.width()
            fill_rect = QRectF(x, rect.y(), w, rect.height()).intersected(rect)
        elif self._value > 0:
            fill_rect = QRectF(rect.x(), rect.y(), rect.width() * self._value, rect.height())
        else:
            return

        fill_path = QPainterPath()
        fill_path.addRoundedRect(fill_rect, r, r)
        painter.fillPath(fill_path, QBrush(self._fill))
