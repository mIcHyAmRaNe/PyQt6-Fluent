from __future__ import annotations

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QAction, QBrush, QColor, QPainter
from PyQt6.QtWidgets import QLineEdit, QSizePolicy

from ...icons.engine import FluentIcon, IconEngine
from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class Input(ThemeAwareWidget, QLineEdit):
    """Windows 11 Fluent TextBox with only a bottom accent border."""

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
        placeholder = r.color("component.input_placeholder")

        self.setStyleSheet(f"""
Input {{
    background-color: {bg.name(QColor.NameFormat.HexArgb)};
    color: {fg.name()};
    border: none;
    border-radius: 0;
    padding: 0 8px;
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 14px;
}}
Input:disabled {{
    opacity: 0.4;
}}
Input::placeholder {{
    color: {placeholder.name(QColor.NameFormat.HexArgb)};
    font-style: normal;
}}
""")

    def paintEvent(self, e):
        super().paintEvent(e)

        from ...tokens.theme import ThemeManager
        theme = ThemeManager.instance().theme()
        r = theme.resolver()
        accent = r.color("semantic.accent")
        border = self._custom_border if self._custom_border else r.color("component.input_border")
        line_color = accent if self.hasFocus() else border
        line_width = 2 if self.hasFocus() else 1

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect())
        line_rect = QRectF(
            rect.x(),
            rect.y() + rect.height() - line_width,
            rect.width(),
            line_width,
        )
        painter.fillRect(line_rect, QBrush(line_color))
        painter.end()


class SearchBox(ThemeAwareWidget, QLineEdit):
    """Windows 11 Fluent SearchBox with search icon + only a bottom accent border."""

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

        self._engine = IconEngine.instance()

        self._search_action = QAction(self)
        self.addAction(self._search_action, QLineEdit.ActionPosition.LeadingPosition)

        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        bg = self._custom_bg if self._custom_bg else r.color("component.input_bg")
        fg = self._custom_fg if self._custom_fg else r.color("component.input_fg")
        placeholder = r.color("component.input_placeholder")

        self._search_action.setIcon(
            self._engine.icon(FluentIcon.SEARCH, color=fg, size=20))

        self.setStyleSheet(f"""
SearchBox {{
    background-color: {bg.name(QColor.NameFormat.HexArgb)};
    color: {fg.name()};
    border: none;
    border-radius: 0;
    padding: 0 8px;
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 14px;
}}
SearchBox:disabled {{
    opacity: 0.4;
}}
SearchBox::placeholder {{
    color: {placeholder.name(QColor.NameFormat.HexArgb)};
}}
""")

    def paintEvent(self, e):
        super().paintEvent(e)

        from ...tokens.theme import ThemeManager
        theme = ThemeManager.instance().theme()
        r = theme.resolver()
        accent = r.color("semantic.accent")
        border = self._custom_border if self._custom_border else r.color("component.input_border")
        line_color = accent if self.hasFocus() else border
        line_width = 2 if self.hasFocus() else 1

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect())
        line_rect = QRectF(
            rect.x(),
            rect.y() + rect.height() - line_width,
            rect.width(),
            line_width,
        )
        painter.fillRect(line_rect, QBrush(line_color))
        painter.end()
