from __future__ import annotations

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QComboBox, QListView, QSizePolicy

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class ComboBox(ThemeAwareWidget, QComboBox):
    qss_role = "fluent_combo"

    def __init__(self, parent=None,
                 bg_color=None, fg_color=None, border_color=None,
                 dropdown_bg=None, item_hover=None):
        super().__init__(parent)
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_border = QColor(border_color) if border_color else None
        self._custom_dropdown_bg = QColor(dropdown_bg) if dropdown_bg else None
        self._custom_item_hover = QColor(item_hover) if item_hover else None

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(32)
        self.setView(QListView())
        self.view().setObjectName("fluent_combo_popup")

        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        bg = self._custom_bg if self._custom_bg else r.color("component.combobox_bg")
        fg = self._custom_fg if self._custom_fg else r.color("component.combobox_fg")
        border = self._custom_border if self._custom_border else r.color("component.combobox_border")
        focus_border = r.color("component.combobox_focus_border")
        dropdown_bg = self._custom_dropdown_bg if self._custom_dropdown_bg else r.color("component.combobox_dropdown_bg")
        item_hover = self._custom_item_hover if self._custom_item_hover else r.color("component.combobox_item_hover")
        item_selected = r.color("component.combobox_item_selected")
        item_selected_fg = r.color("component.combobox_item_selected_fg")
        arrow = r.color("component.combobox_arrow")
        radius = r.int("component.control_radius")

        self.setStyleSheet(f"""
ComboBox {{
    background-color: {bg.name(QColor.NameFormat.HexArgb)};
    color: {fg.name()};
    border: 1px solid {border.name(QColor.NameFormat.HexArgb)};
    border-radius: {radius}px;
    padding: 0 28px 0 8px;
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 14px;
}}
ComboBox:focus {{
    border: 2px solid {focus_border.name()};
    padding: 0 27px 0 7px;
}}
ComboBox:disabled {{
    opacity: 0.4;
}}
ComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border: none;
    border-top-right-radius: {radius}px;
    border-bottom-right-radius: {radius}px;
}}
ComboBox::down-arrow {{
    image: none;
    width: 8px;
    height: 8px;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {arrow.name()};
}}
ComboBox QAbstractItemView {{
    background-color: {dropdown_bg.name(QColor.NameFormat.HexArgb)};
    color: {fg.name()};
    border: 1px solid {border.name(QColor.NameFormat.HexArgb)};
    border-radius: {radius}px;
    padding: 4px 0;
    outline: none;
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 14px;
}}
ComboBox QAbstractItemView::item {{
    padding: 4px 12px;
    min-height: 24px;
}}
ComboBox QAbstractItemView::item:hover {{
    background-color: {item_hover.name(QColor.NameFormat.HexArgb)};
}}
ComboBox QAbstractItemView::item:selected {{
    background-color: {item_selected.name(QColor.NameFormat.HexArgb)};
    color: {item_selected_fg.name()};
}}
""")
