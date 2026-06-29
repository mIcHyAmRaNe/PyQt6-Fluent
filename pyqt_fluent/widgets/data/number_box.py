from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QBrush, QPen, QMouseEvent
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QSizePolicy, QWidget

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class _ArrowButton(QWidget):
    def __init__(self, parent, up=True):
        super().__init__(parent)
        self.setFixedSize(20, 14)
        self._up = up
        self._hovered = False
        self._pressed = False
        self.setMouseTracking(True)

    def enterEvent(self, e):
        self._hovered = True
        self.update()

    def leaveEvent(self, e):
        self._hovered = False
        self._pressed = False
        self.update()

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.MouseButton.LeftButton:
            self._pressed = True
            self.update()

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.MouseButton.LeftButton and self._pressed:
            self._pressed = False
            self.update()
            nb: NumberBox = self.parent().parent() if self.parent() else None
            if nb:
                if self._up:
                    nb._step_up()
                else:
                    nb._step_down()

    def paintEvent(self, e):
        nb: NumberBox = self.parent().parent() if self.parent() else None
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        r = self.rect()
        bg = nb._button_bg if nb else QColor(200, 200, 200)
        if self._pressed:
            bg = nb._button_pressed if nb else bg
        elif self._hovered:
            bg = nb._button_hover if nb else bg
        path = QPainterPath()
        path.addRoundedRect(QRectF(r), 2, 2)
        painter.fillPath(path, QBrush(bg))

        fg = nb._fg if nb else QColor(0, 0, 0)
        painter.setPen(QPen(fg, 1.5))
        painter.setBrush(QBrush(fg))
        cx, cy = r.width() / 2, r.height() / 2
        s = 4
        tri = QPainterPath()
        if self._up:
            tri.moveTo(cx, cy - s)
            tri.lineTo(cx - s, cy + s)
            tri.lineTo(cx + s, cy + s)
        else:
            tri.moveTo(cx, cy + s)
            tri.lineTo(cx - s, cy - s)
            tri.lineTo(cx + s, cy - s)
        tri.closeSubpath()
        painter.drawPath(tri)


class NumberBox(ThemeAwareWidget, QWidget):
    value_changed = pyqtSignal(float)

    def __init__(self, parent=None,
                 bg_color=None, fg_color=None, border_color=None,
                 button_bg=None, button_hover=None, button_pressed=None,
                 min_value=0, max_value=100, step=1, value=0):
        super().__init__(parent)
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_border = QColor(border_color) if border_color else None
        self._custom_button_bg = QColor(button_bg) if button_bg else None
        self._custom_button_hover = QColor(button_hover) if button_hover else None
        self._custom_button_pressed = QColor(button_pressed) if button_pressed else None

        self._bg = QColor()
        self._fg = QColor()
        self._border = QColor()
        self._button_bg = QColor()
        self._button_hover = QColor()
        self._button_pressed = QColor()

        self._min = min_value
        self._max = max_value
        self._step = step
        self._value = float(value)

        self.setFixedHeight(32)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._input = QLineEdit()
        self._input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._input.setText(self._format_value(self._value))
        self._input.setFixedHeight(32)
        self._input.returnPressed.connect(self._on_text_entered)
        layout.addWidget(self._input, 1)

        btn_layout = QVBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(0)

        self._up_btn = _ArrowButton(self, up=True)
        self._down_btn = _ArrowButton(self, up=False)
        btn_layout.addWidget(self._up_btn)
        btn_layout.addWidget(self._down_btn)

        wrapper = QWidget()
        wrapper.setLayout(btn_layout)
        wrapper.setFixedWidth(20)
        layout.addWidget(wrapper)

        self._init_theme_aware()

    def value(self) -> float:
        return self._value

    def set_value(self, v: float, emit=True):
        self._value = max(self._min, min(self._max, v))
        self._value = round(self._value / self._step) * self._step
        self._input.setText(self._format_value(self._value))
        if emit:
            self.value_changed.emit(self._value)
        self.update()

    def set_range(self, min_val: float, max_val: float):
        self._min = min_val
        self._max = max_val
        self.set_value(self._value)

    def set_step(self, s: float):
        self._step = s

    def _format_value(self, v: float) -> str:
        if self._step == int(self._step):
            return str(int(v))
        return f"{v:.{max(0, len(str(self._step).split('.')[1]))}f}"

    def _step_up(self):
        self.set_value(self._value + self._step)

    def _step_down(self):
        self.set_value(self._value - self._step)

    def _on_text_entered(self):
        try:
            v = float(self._input.text())
            self.set_value(v)
        except ValueError:
            self._input.setText(self._format_value(self._value))

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        c = theme.component
        self._bg = self._custom_bg if self._custom_bg else r.color(c.numberbox_bg)
        self._fg = self._custom_fg if self._custom_fg else r.color(c.numberbox_fg)
        self._border = self._custom_border if self._custom_border else r.color(c.numberbox_border)
        self._button_bg = self._custom_button_bg if self._custom_button_bg else r.color(c.numberbox_button_bg)
        self._button_hover = self._custom_button_hover if self._custom_button_hover else r.color(c.numberbox_button_hover)
        self._button_pressed = self._custom_button_pressed if self._custom_button_pressed else r.color(c.numberbox_button_pressed)
        focus_border = r.color(c.numberbox_focus_border)
        radius = r.int("component.control_radius")
        bg = self._bg.name(QColor.NameFormat.HexArgb)
        fg = self._fg.name()
        border = self._border.name(QColor.NameFormat.HexArgb)
        self._input.setStyleSheet(f"""
QLineEdit {{
    background-color: {bg};
    color: {fg};
    border: 1px solid {border};
    border-radius: {radius}px;
    padding: 0 8px;
    font-size: 14px;
}}
QLineEdit:focus {{
    border: 1px solid {focus_border.name()};
}}
""")

    def paintEvent(self, e):
        pass
