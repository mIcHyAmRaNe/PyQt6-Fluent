from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import QSizePolicy, QWidget

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class SpinBox(ThemeAwareWidget, QWidget):
    """Number input with +/- buttons matching FluSpinBox.qml."""

    def __init__(self, parent=None, value=0, min_val=0, max_val=999, step=1):
        super().__init__(parent)
        self._value = value
        self._min = min_val
        self._max = max_val
        self._step = step
        self._hovered = False
        self._pressed_btn = None  # "up" or "down"
        self._bg = QColor()
        self._bg_hover = QColor()
        self._bg_focused = QColor()
        self._bg_disabled = QColor()
        self._button_bg = QColor()
        self._button_hover = QColor()
        self._button_pressed = QColor()
        self._border_color = QColor()
        self._border_disabled = QColor()
        self._fg = QColor()
        self._accent = QColor()

        self.setFixedHeight(32)
        self.setFixedWidth(136)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setMouseTracking(True)
        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._bg = r.color("palette.spinbox_bg")
        self._bg_hover = r.color("palette.spinbox_bg_hover")
        self._bg_focused = r.color("palette.spinbox_bg_focused")
        self._bg_disabled = r.color("palette.spinbox_bg_disabled")
        self._button_bg = r.color("palette.spinbox_button_bg")
        self._button_hover = r.color("palette.spinbox_button_hover")
        self._button_pressed = r.color("palette.spinbox_button_pressed")
        self._border_color = r.color("palette.spinbox_border")
        self._border_disabled = r.color("palette.spinbox_border_disabled")
        self._fg = r.color("palette.textbox_text")
        self._accent = r.color("semantic.accent")
        self.update()

    def value(self) -> int:
        return self._value

    def setValue(self, v: int):
        self._value = max(self._min, min(self._max, v))
        self.update()

    def _up_rect(self) -> QRectF:
        return QRectF(self.width() - 32, 0, 32, self.height())

    def _down_rect(self) -> QRectF:
        return QRectF(0, 0, 32, self.height())

    def _input_rect(self) -> QRectF:
        return QRectF(32, 0, self.width() - 64, self.height())

    def mousePressEvent(self, e):
        if self._up_rect().contains(e.position()):
            self._pressed_btn = "up"
            self.setValue(self._value + self._step)
        elif self._down_rect().contains(e.position()):
            self._pressed_btn = "down"
            self.setValue(self._value - self._step)
        self.update()

    def mouseReleaseEvent(self, e):
        self._pressed_btn = None
        self.update()

    def mouseMoveEvent(self, e):
        self._hovered = self.rect().contains(e.rect())
        self.update()

    def leaveEvent(self, e):
        self._hovered = False
        self._pressed_btn = None
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect())
        bg = self._bg

        # Background
        bg_path = QPainterPath()
        bg_path.addRoundedRect(rect, 4, 4)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(bg))
        painter.drawPath(bg_path)

        # Border
        border = self._border_color
        painter.setPen(QPen(border, 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(bg_path)

        # Up button
        up = self._up_rect()
        up_bg = self._button_pressed if self._pressed_btn == "up" else (
            self._button_hover if up.contains(self.mapFromGlobal(
                self.cursor().pos())) else self._button_bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(up_bg))
        painter.drawRect(up)

        # Up +/- symbol
        painter.setPen(QPen(self._fg, 2))
        cx, cy = up.center().x(), up.center().y()
        painter.drawLine(int(cx - 5), int(cy), int(cx + 5), int(cy))
        if self._value < self._max:
            painter.drawLine(int(cx), int(cy - 5), int(cx), int(cy + 5))

        # Down button
        down = self._down_rect()
        down_bg = self._button_pressed if self._pressed_btn == "down" else (
            self._button_hover if down.contains(self.mapFromGlobal(
                self.cursor().pos())) else self._button_bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(down_bg))
        painter.drawRect(down)

        # Down - symbol
        painter.setPen(QPen(self._fg, 2))
        cx, cy = down.center().x(), down.center().y()
        painter.drawLine(int(cx - 5), int(cy), int(cx + 5), int(cy))

        # Value text
        painter.setPen(self._fg)
        painter.setFont(QFont("Segoe UI Variable", 14))
        input_rect = self._input_rect()
        painter.drawText(input_rect, Qt.AlignmentFlag.AlignCenter, str(self._value))

        # Bottom accent line
        if self.hasFocus():
            painter.setPen(QPen(self._accent, 2))
            painter.drawLine(int(rect.x()), int(rect.height() - 1),
                             int(rect.width()), int(rect.height() - 1))

        painter.end()

    def sizeHint(self):
        return (136, 32)
