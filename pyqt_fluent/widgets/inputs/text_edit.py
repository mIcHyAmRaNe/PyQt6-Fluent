from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QPlainTextEdit, QSizePolicy

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class Textarea(ThemeAwareWidget, QPlainTextEdit):
    qss_role = "fluent_textarea"

    def __init__(self, text="", parent=None,
                 bg_color=None, fg_color=None, border_color=None):
        super().__init__(parent)
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_border = QColor(border_color) if border_color else None
        self.setPlainText(text)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(64)
        self.setTabChangesFocus(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        bg = self._custom_bg if self._custom_bg else r.color("component.input_bg")
        fg = self._custom_fg if self._custom_fg else r.color("component.input_fg")
        border = self._custom_border if self._custom_border else r.color("component.input_border")
        focus_border = r.color("component.input_focus_border")
        radius = r.int("component.control_radius")
        self.setStyleSheet(f"""
Textarea {{
    background-color: {bg.name(QColor.NameFormat.HexArgb)};
    color: {fg.name()};
    border: 1px solid {border.name(QColor.NameFormat.HexArgb)};
    border-radius: {radius}px;
    padding: 4px 8px;
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 14px;
}}
Textarea:focus {{
    border: 1px solid {focus_border.name()};
}}
Textarea:disabled {{
    opacity: 0.4;
}}
""")
