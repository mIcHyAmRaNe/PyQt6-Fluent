from __future__ import annotations

from PyQt6.QtCore import Qt, QRectF, QTimer, QPoint
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QBrush, QFont, QPen
from PyQt6.QtWidgets import QWidget, QApplication

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class FluentTooltip(ThemeAwareWidget, QWidget):
    def __init__(self, parent=None, text="", bg_color=None, fg_color=None):
        super().__init__(parent)
        self._text = text
        self._bg = QColor()
        self._fg = QColor()
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._arrow_size = 8
        self._padding = 8
        self._radius = 6

        self.setWindowFlags(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.hide)

        self._init_theme_aware()

    def set_text(self, text: str):
        self._text = text
        self.adjustSize()
        self.update()

    def show_for(self, widget: QWidget, text: str = "", duration: int = 3000):
        if text:
            self._text = text
        self.adjustSize()

        pos = widget.mapToGlobal(QPoint(0, 0))
        below = pos.y() + widget.height() + 4
        screen = QApplication.primaryScreen().availableGeometry()
        if below + self.height() > screen.bottom():
            below = pos.y() - self.height() - 4
        self.move(pos.x() + (widget.width() - self.width()) // 2, below)
        self.show()
        self.raise_()

        if duration > 0:
            self._hide_timer.start(duration)

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._bg = self._custom_bg if self._custom_bg else r.color("component.tooltip_bg")
        self._fg = self._custom_fg if self._custom_fg else r.color("component.tooltip_fg")
        self.update()

    def sizeHint(self):
        from PyQt6.QtCore import QSize
        font = QFont("Segoe UI Variable, Segoe UI, sans-serif")
        font.setPixelSize(12)
        fm = self.fontMetrics()
        tw = fm.horizontalAdvance(self._text or "")
        th = fm.height()
        return QSize(int(tw + self._padding * 2 + 2), int(th + self._padding * 2 + self._arrow_size + 2))

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        body = rect.adjusted(0, self._arrow_size, 0, 0)
        path = QPainterPath()
        path.addRoundedRect(body, self._radius, self._radius)

        arrow_cx = rect.width() / 2
        arrow_path = QPainterPath()
        arrow_path.moveTo(arrow_cx - self._arrow_size, self._arrow_size)
        arrow_path.lineTo(arrow_cx, 0)
        arrow_path.lineTo(arrow_cx + self._arrow_size, self._arrow_size)
        arrow_path.closeSubpath()
        path = path.united(arrow_path)

        painter.fillPath(path, QBrush(self._bg))

        font = QFont("Segoe UI Variable, Segoe UI, sans-serif")
        font.setPixelSize(12)
        painter.setFont(font)
        painter.setPen(self._fg)
        text_rect = body.adjusted(self._padding, self._padding, -self._padding, -self._padding)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._text)
