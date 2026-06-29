from __future__ import annotations

from PyQt6.QtCore import Qt, QRectF, QSize
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QBrush, QFont
from PyQt6.QtWidgets import QWidget, QSizePolicy

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class Avatar(ThemeAwareWidget, QWidget):
    def __init__(self, parent=None, text="", size=40, bg_color=None, fg_color=None):
        super().__init__(parent)
        self._text = text
        self._size = size
        self._bg = QColor()
        self._fg = QColor()
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None

        self.setFixedSize(size, size)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._init_theme_aware()

    def _initials(self) -> str:
        parts = self._text.strip().split()
        chars = [p[0].upper() for p in parts if p]
        return "".join(chars[:2])

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._bg = self._custom_bg if self._custom_bg else r.color("component.avatar_bg")
        self._fg = self._custom_fg if self._custom_fg else r.color("component.avatar_fg")
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect())
        path = QPainterPath()
        path.addEllipse(rect)
        painter.setClipPath(path)
        painter.fillPath(path, QBrush(self._bg))

        initials = self._initials()
        font_size = max(10, self._size // 2)
        font = QFont("Segoe UI Variable, Segoe UI, sans-serif")
        font.setPixelSize(font_size)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(self._fg)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, initials)
