"""ToggleButton — checkable push button with Win11 states."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPainter
from PyQt6.QtWidgets import QSizePolicy

from ._base import ButtonBase


class ToggleButton(ButtonBase):
    """Checkable push button — toggles between unchecked / accent fill.

    Win11 behaviour:
      - Unchecked: transparent bg (subtle_fill rest)
      - Checked:   accent bg
      - Hover/press animate within each branch.
    """

    control_tokens_key = "button_standard"
    fg_ref = "semantic.control_fg"
    border_ref = "semantic.control_border"

    def __init__(self, text="", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setCheckable(True)
        self.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Fixed,
        )

    def _unchecked_bg(self) -> str:
        return "semantic.subtle_fill"

    def _checked_bg(self) -> str:
        return "semantic.accent"

    def on_theme_applied(self, theme):
        super().on_theme_applied(theme)
        r = theme.resolver()
        # Override checked rest/hover/pressed with accent colours
        self._bg_pressed = r.color("semantic.accent_pressed")
        if self.isChecked():
            self._bg_rest = r.color("semantic.accent")
            self._bg_hover = r.color("semantic.accent_hover")
            self._fg = r.color("semantic.on_accent")
        else:
            unchecked = r.color(self._unchecked_bg())
            self._bg_rest = unchecked
            self._bg_hover = r.color("semantic.hover")
            self._fg = r.color("semantic.control_fg")

    def nextCheckState(self):
        super().nextCheckState()
        self.on_theme_applied(self._current_theme())
        # Animate from current bg to new state colour
        self._start_bg_animation()

    def _current_theme(self):
        from ...tokens.theme import ThemeManager
        return ThemeManager.instance().theme()

    def _draw_indicator(self, painter: QPainter) -> None:
        self._draw_background(painter)
        painter.setPen(self._fg)
        f = QFont()
        f.setPixelSize(14)
        painter.setFont(f)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
