from __future__ import annotations

from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QBrush, QPen, QFont
from PyQt6.QtWidgets import QWidget, QSizePolicy

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class Tag(ThemeAwareWidget, QWidget):
    qss_role = "fluent_tag"
    closed = pyqtSignal()

    def __init__(self, text="", closable=False, parent=None,
                 bg_color=None, fg_color=None):
        super().__init__(parent)
        self._text = text
        self._closable = closable
        self._bg = QColor()
        self._fg = QColor()
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._hover_close = False
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._bg = self._custom_bg if self._custom_bg else r.color("semantic.subtle_fill")
        self._fg = self._custom_fg if self._custom_fg else r.color("semantic.control_fg")
        self.update()

    def sizeHint(self):
        from PyQt6.QtCore import QSize
        fm = self.fontMetrics()
        tw = fm.horizontalAdvance(self._text or " ")
        w = tw + 16
        if self._closable:
            w += 20
        return QSize(w, 24)

    def mouseMoveEvent(self, e):
        if self._closable:
            close_rect = QRectF(self.width() - 20, 0, 20, self.height())
            self._hover_close = close_rect.contains(e.position())
            self.update()

    def leaveEvent(self, e):
        self._hover_close = False
        self.update()

    def mousePressEvent(self, e):
        if self._closable and e.button() == Qt.MouseButton.LeftButton:
            close_rect = QRectF(self.width() - 20, 0, 20, self.height())
            if close_rect.contains(e.position()):
                self.closed.emit()
                return
        e.ignore()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect()).adjusted(0, 0, 0, 0)
        path = QPainterPath()
        path.addRoundedRect(rect, 4, 4)
        painter.fillPath(path, QBrush(self._bg))

        font = QFont("Segoe UI Variable, Segoe UI, sans-serif")
        font.setPixelSize(12)
        painter.setFont(font)

        painter.setPen(self._fg)
        text_rect = QRectF(8, 0, self.width() - 16 - (20 if self._closable else 0), self.height())
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._text or "")

        if self._closable:
            cx = self.width() - 12
            cy = self.height() / 2
            pen = QPen(self._fg, 1.5)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            painter.drawLine(int(cx - 3), int(cy - 3), int(cx + 3), int(cy + 3))
            painter.drawLine(int(cx + 3), int(cy - 3), int(cx - 3), int(cy + 3))
