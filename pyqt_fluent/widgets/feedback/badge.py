from __future__ import annotations

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QBrush, QFont
from PyQt6.QtWidgets import QWidget, QSizePolicy

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class Badge(ThemeAwareWidget, QWidget):
    qss_role = "fluent_badge"

    def __init__(self, text="", parent=None,
                 bg_color=None, fg_color=None, radius=None):
        super().__init__(parent)
        self._text = text
        self._bg = QColor()
        self._fg = QColor()
        self._radius = radius
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._dot = not text
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._init_theme_aware()

    def set_text(self, text: str):
        self._text = text
        self._dot = not text
        self.adjustSize()
        self.update()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._bg = self._custom_bg if self._custom_bg else r.color("semantic.accent")
        self._fg = self._custom_fg if self._custom_fg else r.color("semantic.on_accent")
        self.adjustSize()
        self.update()

    def sizeHint(self):
        from PyQt6.QtCore import QSize
        if self._dot:
            return QSize(10, 10)
        font = QFont("Segoe UI Variable, Segoe UI, sans-serif")
        font.setPixelSize(12)
        fm = self.fontMetrics()
        tw = fm.horizontalAdvance(self._text or "0")
        th = fm.height()
        bw = max(tw + 12, 20)
        bh = th + 4
        return QSize(int(bw), int(bh))

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._dot:
            rect = QRectF(self.rect()).adjusted(2, 2, -2, -2)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(self._bg))
            painter.drawEllipse(rect)
            return

        font = QFont("Segoe UI Variable, Segoe UI, sans-serif")
        font.setPixelSize(12)
        painter.setFont(font)

        text = self._text or "0"
        fm = painter.fontMetrics()
        tw = fm.horizontalAdvance(text)
        th = fm.height()
        bw = max(tw + 12, 20)
        bh = th + 4

        rect = QRectF(0, 0, bw, bh)
        r = self._radius if self._radius is not None else bh / 2
        path = QPainterPath()
        path.addRoundedRect(rect, r, r)
        painter.fillPath(path, QBrush(self._bg))

        painter.setPen(self._fg)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
