from __future__ import annotations

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QBrush, QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import QFrame, QSizePolicy

from ...tokens.theme import ThemeDefinition
from .._shared.shadow import DropShadow
from .._shared.theme_aware import ThemeAwareWidget


class Card(ThemeAwareWidget, QFrame):
    qss_role = ""

    def __init__(self, parent=None,
                 bg_color=None, radius=None):
        super().__init__(parent)
        self._bg = QColor()
        self._radius = 8
        self._shadow_color = QColor()
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_radius = radius
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._bg = self._custom_bg if self._custom_bg else r.color("component.card_bg")
        self._radius = (self._custom_radius if self._custom_radius is not None
                        else r.int("component.window_radius"))
        self._shadow_color = QColor(0, 0, 0, 30) if theme.is_dark else QColor(0, 0, 0, 15)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5),
                            self._radius, self._radius)
        painter.fillPath(path, QBrush(self._bg))

        DropShadow.paint(painter, QRectF(self.rect()),
                         self._shadow_color, self._radius)
