from __future__ import annotations

from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QLabel

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class FluentLabel(ThemeAwareWidget, QLabel):
    """Label with Fluent 2 typography."""

    qss_role = "fluent_label"

    PRESETS = {
        "caption": {"size": 12, "weight": QFont.Weight.Normal},
        "body": {"size": 14, "weight": QFont.Weight.Normal},
        "body_strong": {"size": 14, "weight": QFont.Weight.DemiBold},
        "body_large": {"size": 16, "weight": QFont.Weight.Normal},
        "subtitle": {"size": 20, "weight": QFont.Weight.DemiBold},
        "title": {"size": 24, "weight": QFont.Weight.DemiBold},
        "title_large": {"size": 32, "weight": QFont.Weight.DemiBold},
        "display": {"size": 48, "weight": QFont.Weight.DemiBold},
    }

    def __init__(self, text="", preset="body", parent=None):
        super().__init__(text, parent)
        self._preset = preset
        self._fg = QColor()
        self._init_theme_aware()

    def set_preset(self, preset: str):
        self._preset = preset
        self._apply_font()
        self.update()

    def _apply_font(self):
        p = self.PRESETS.get(self._preset, self.PRESETS["body"])
        font = QFont("Segoe UI Variable, Segoe UI, sans-serif")
        font.setPixelSize(p["size"])
        font.setWeight(p["weight"])
        self.setFont(font)

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        if self._preset in ("caption",):
            self._fg = r.color("semantic.on_surface_muted")
        else:
            self._fg = r.color("component.content_fg")
        self._apply_font()
        self.setStyleSheet(f"""
FluentLabel {{
    color: {self._fg.name()};
    background: transparent;
}}
FluentLabel:disabled {{
    opacity: 0.4;
}}
""")
