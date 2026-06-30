from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget

from ...tokens.theme import ThemeDefinition, ThemeManager
from .._shared.theme_aware import ThemeAwareWidget

_SEVERITY_KEYS = {
    "info": "infobar_info",
    "success": "infobar_success",
    "warning": "infobar_warning",
    "danger": "infobar_danger",
}


class InfoBar(ThemeAwareWidget, QWidget):
    dismissed = pyqtSignal()

    def __init__(self, text="", severity="info", parent=None,
                 bg_color=None, fg_color=None, closable=True, duration=0):
        super().__init__(parent)
        self._text = text
        self._severity = severity if severity in _SEVERITY_KEYS else "info"
        self._closable = closable

        self._bg = QColor()
        self._fg = QColor()
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._border_color = QColor()

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(12, 8, 8, 8)
        self._layout.setSpacing(8)

        self._label = QLabel(text)
        self._label.setWordWrap(True)
        self._layout.addWidget(self._label, 1)

        if closable:
            self._close_btn = QPushButton("✕")
            self._close_btn.setFixedSize(24, 24)
            self._close_btn.setFlat(True)
            self._close_btn.setToolTip("Close")
            self._close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self._close_btn.clicked.connect(self.dismiss)
            self._layout.addWidget(self._close_btn)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        if duration > 0:
            self._timer = QTimer(self)
            self._timer.setSingleShot(True)
            self._timer.timeout.connect(self.dismiss)
            self._timer.start(duration)
        else:
            self._timer = None

        self._init_theme_aware()

    def set_text(self, text: str):
        self._text = text
        self._label.setText(text)

    def set_severity(self, severity: str):
        self._severity = severity if severity in _SEVERITY_KEYS else "info"
        self.on_theme_applied(ThemeManager.instance().theme())
        self.update()

    def dismiss(self):
        self.dismissed.emit()
        self.hide()

    def show(self):
        super().show()
        if self._timer and not self._timer.isActive():
            pass

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        key = _SEVERITY_KEYS.get(self._severity, "infobar_info")
        self._bg = self._custom_bg if self._custom_bg else r.color(f"component.{key}_bg")
        self._fg = self._custom_fg if self._custom_fg else r.color(f"component.{key}_fg")
        self._border_color = r.color("component.infobar_border")
        self._label.setStyleSheet(f"color: {self._fg.name()}; background: transparent;")
        if self._closable:
            self._close_btn.setStyleSheet(
                f"color: {self._fg.name()}; background: transparent; border: none; font-size: 14px;"
            )
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        r = 4
        path.addRoundedRect(rect, r, r)
        painter.fillPath(path, QBrush(self._bg))

        pen = QPen(self._border_color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)
