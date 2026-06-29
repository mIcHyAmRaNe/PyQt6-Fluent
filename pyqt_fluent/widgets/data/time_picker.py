from __future__ import annotations

from PyQt6.QtCore import QRectF, QTime, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QBrush, QPen
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSpinBox, QVBoxLayout, QWidget, QFrame

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class _TimePopup(ThemeAwareWidget, QFrame):
    time_selected = pyqtSignal(QTime)

    def __init__(self, parent=None, popup_bg=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(180, 120)

        self._custom_popup_bg = QColor(popup_bg) if popup_bg else None
        self._popup_bg = QColor()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        spin_layout = QHBoxLayout()
        spin_layout.setSpacing(4)

        self._hour_spin = QSpinBox()
        self._hour_spin.setRange(0, 23)
        self._hour_spin.setFixedSize(60, 28)
        self._hour_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sep = QLabel(":")
        sep.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sep.setFixedWidth(12)

        self._min_spin = QSpinBox()
        self._min_spin.setRange(0, 59)
        self._min_spin.setFixedSize(60, 28)
        self._min_spin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        spin_layout.addStretch()
        spin_layout.addWidget(self._hour_spin)
        spin_layout.addWidget(sep)
        spin_layout.addWidget(self._min_spin)
        spin_layout.addStretch()
        layout.addLayout(spin_layout)

        self._ok_btn = QPushButton("OK")
        self._ok_btn.setFixedHeight(28)
        self._ok_btn.clicked.connect(self._confirm)
        layout.addWidget(self._ok_btn)

        self._init_theme_aware()

    def set_time(self, t: QTime):
        self._hour_spin.setValue(t.hour())
        self._min_spin.setValue(t.minute())

    def _confirm(self):
        t = QTime(self._hour_spin.value(), self._min_spin.value())
        self.time_selected.emit(t)

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        c = theme.component
        self._popup_bg = self._custom_popup_bg if self._custom_popup_bg else r.color(c.picker_popup_bg)
        fg = r.color(c.picker_fg)
        bg = r.color(c.picker_bg)
        border = r.color(c.picker_border)
        radius = r.int("component.control_radius")
        self.setStyleSheet(f"""
QFrame {{
    background: {self._popup_bg.name(QColor.NameFormat.HexArgb)};
    border-radius: 8px;
}}
QSpinBox {{
    background-color: {bg.name(QColor.NameFormat.HexArgb)};
    color: {fg.name()};
    border: 1px solid {border.name(QColor.NameFormat.HexArgb)};
    border-radius: {radius}px;
    padding: 2px 4px;
    font-size: 14px;
}}
QSpinBox::up-button, QSpinBox::down-button {{
    width: 16px;
    border: none;
    background: transparent;
}}
QSpinBox::up-arrow {{
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-bottom: 5px solid {fg.name()};
}}
QSpinBox::down-arrow {{
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {fg.name()};
}}
QPushButton {{
    background-color: {bg.name(QColor.NameFormat.HexArgb)};
    color: {fg.name()};
    border: 1px solid {border.name(QColor.NameFormat.HexArgb)};
    border-radius: {radius}px;
    font-size: 13px;
}}
QPushButton:hover {{
    background: {r.color("semantic.hover").name(QColor.NameFormat.HexArgb)};
}}
QPushButton:pressed {{
    background: {r.color("semantic.pressed").name(QColor.NameFormat.HexArgb)};
}}
QLabel {{
    color: {fg.name()};
    background: transparent;
    font-size: 16px;
    font-weight: bold;
}}
""")

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 8, 8)
        painter.fillPath(path, QBrush(self._popup_bg))


class TimePicker(ThemeAwareWidget, QWidget):
    time_changed = pyqtSignal(QTime)

    def __init__(self, parent=None,
                 bg_color=None, fg_color=None, border_color=None,
                 popup_bg=None):
        super().__init__(parent)
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_border = QColor(border_color) if border_color else None

        self._bg = QColor()
        self._fg = QColor()
        self._border = QColor()

        self._time = QTime.currentTime()

        self.setFixedHeight(32)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 4, 0)

        self._label = QLabel(self._time.toString("HH:mm"))
        self._label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self._label, 1)

        self._arrow = QPushButton("▼")
        self._arrow.setFixedSize(24, 24)
        self._arrow.setFlat(True)
        self._arrow.clicked.connect(self._toggle_popup)
        layout.addWidget(self._arrow)

        self._popup = _TimePopup(self, popup_bg=popup_bg)
        self._popup.time_selected.connect(self._on_time_selected)

        self._init_theme_aware()

    def time(self) -> QTime:
        return self._time

    def set_time(self, t: QTime):
        self._time = t
        self._label.setText(t.toString("HH:mm"))
        self.time_changed.emit(t)
        self.update()

    def _toggle_popup(self):
        if self._popup.isVisible():
            self._popup.hide()
        else:
            pos = self.mapToGlobal(self.rect().bottomLeft())
            self._popup.move(pos)
            self._popup.set_time(self._time)
            self._popup.show()

    def _on_time_selected(self, t: QTime):
        self.set_time(t)
        self._popup.hide()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        c = theme.component
        self._bg = self._custom_bg if self._custom_bg else r.color(c.picker_bg)
        self._fg = self._custom_fg if self._custom_fg else r.color(c.picker_fg)
        self._border = self._custom_border if self._custom_border else r.color(c.picker_border)
        radius = r.int("component.control_radius")
        bg = self._bg.name(QColor.NameFormat.HexArgb)
        fg = self._fg.name()
        border = self._border.name(QColor.NameFormat.HexArgb)
        self.setStyleSheet(f"""
TimePicker {{
    background-color: {bg};
    border: 1px solid {border};
    border-radius: {radius}px;
}}
TimePicker QLabel {{
    color: {fg};
    background: transparent;
    font-size: 14px;
}}
TimePicker QPushButton {{
    color: {fg};
    background: transparent;
    border: none;
    font-size: 10px;
}}
""")

    def paintEvent(self, e):
        pass
