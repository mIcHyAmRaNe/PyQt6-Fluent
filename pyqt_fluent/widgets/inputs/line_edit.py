from __future__ import annotations

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QLineEdit, QSizePolicy

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class Input(ThemeAwareWidget, QLineEdit):
    qss_role = "fluent_input"

    def __init__(self, text="", parent=None,
                 bg_color=None, fg_color=None, border_color=None):
        super().__init__(text, parent)
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_border = QColor(border_color) if border_color else None
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(32)
        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        bg = self._custom_bg if self._custom_bg else r.color("component.input_bg")
        fg = self._custom_fg if self._custom_fg else r.color("component.input_fg")
        border = self._custom_border if self._custom_border else r.color("component.input_border")
        focus_border = r.color("component.input_focus_border")
        placeholder = r.color("component.input_placeholder")
        radius = r.int("component.control_radius")
        self.setStyleSheet(f"""
Input {{
    background-color: {bg.name(QColor.NameFormat.HexArgb)};
    color: {fg.name()};
    border: 1px solid {border.name(QColor.NameFormat.HexArgb)};
    border-radius: {radius}px;
    padding: 0 8px;
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 14px;
}}
Input:focus {{
    border: 1px solid {focus_border.name()};
}}
Input:disabled {{
    opacity: 0.4;
}}
Input::placeholder {{
    color: {placeholder.name(QColor.NameFormat.HexArgb)};
    font-style: normal;
}}
""")


class SearchBox(ThemeAwareWidget, QLineEdit):
    qss_role = "fluent_search"

    def __init__(self, text="", parent=None,
                 bg_color=None, fg_color=None, border_color=None):
        super().__init__(text, parent)
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_border = QColor(border_color) if border_color else None
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(32)
        self.setClearButtonEnabled(True)

        from PyQt6.QtGui import QAction, QIcon
        self._search_action = QAction(self)
        self._search_action.setIcon(QIcon())
        self.addAction(self._search_action, QLineEdit.ActionPosition.LeadingPosition)

        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        bg = self._custom_bg if self._custom_bg else r.color("component.input_bg")
        fg = self._custom_fg if self._custom_fg else r.color("component.input_fg")
        border = self._custom_border if self._custom_border else r.color("component.input_border")
        focus_border = r.color("component.input_focus_border")
        placeholder = r.color("component.input_placeholder")
        radius = r.int("component.control_radius")
        qss = f"""
SearchBox {{
    background-color: {bg.name(QColor.NameFormat.HexArgb)};
    color: {fg.name()};
    border: 1px solid {border.name(QColor.NameFormat.HexArgb)};
    border-radius: {radius}px;
    padding: 0 8px 0 32px;
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 14px;
}}
SearchBox:focus {{
    border: 1px solid {focus_border.name()};
}}
SearchBox:disabled {{
    opacity: 0.4;
}}
SearchBox::placeholder {{
    color: {placeholder.name(QColor.NameFormat.HexArgb)};
}}
"""
        self.setStyleSheet(qss)
