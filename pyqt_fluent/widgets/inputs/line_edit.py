from __future__ import annotations

from importlib.resources import files as _resources

from PyQt6.QtCore import QFile
from PyQt6.QtGui import QColor, QIcon, QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QLineEdit, QSizePolicy

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


def _make_colored_icon(svg_path: str, color: QColor, size: int = 20) -> QIcon:
    f = QFile(svg_path)
    if not f.open(QFile.OpenModeFlag.ReadOnly):
        return QIcon()
    data = f.readAll()
    f.close()

    pix = QPixmap(size, size)
    pix.fill(QColor(0, 0, 0, 0))
    renderer = QSvgRenderer(data)
    painter = QPainter(pix)
    renderer.render(painter)
    painter.setCompositionMode(
        QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pix.rect(), color)
    painter.end()
    return QIcon(pix)


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

        p = _resources("pyqt_fluent.resources").joinpath("icons", "Search_filled.svg")
        self._search_svg_path = str(p)

        from PyQt6.QtGui import QAction
        self._search_action = QAction(self)
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

        self._search_action.setIcon(
            _make_colored_icon(self._search_svg_path, fg, 20))

        qss = f"""
SearchBox {{
    background-color: {bg.name(QColor.NameFormat.HexArgb)};
    color: {fg.name()};
    border: 1px solid {border.name(QColor.NameFormat.HexArgb)};
    border-radius: {radius}px;
    padding: 0 8px;
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

