from __future__ import annotations

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QBrush, QColor, QPainter
from PyQt6.QtWidgets import QLineEdit, QSizePolicy

from ...icons.engine import FluentIcon, IconEngine
from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class PasswordBox(ThemeAwareWidget, QLineEdit):
    """Windows 11 Fluent PasswordBox with reveal toggle button."""

    qss_role = "fluent_input"

    def __init__(self, text="", parent=None,
                 bg_color=None, fg_color=None, border_color=None):
        super().__init__(text, parent)
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_border = QColor(border_color) if border_color else None
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(32)
        self.setEchoMode(QLineEdit.EchoMode.Password)

        self._engine = IconEngine.instance()
        self._revealed = False

        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        bg = self._custom_bg if self._custom_bg else r.color("component.input_bg")
        fg = self._custom_fg if self._custom_fg else r.color("component.input_fg")
        placeholder = r.color("component.input_placeholder")
        self._fg = fg

        reveal_icon = self._engine.icon(
            FluentIcon.VISIBILITY if not self._revealed else FluentIcon.HIDE,
            color=fg, size=16)

        self.setStyleSheet(f"""
PasswordBox {{
    background-color: {bg.name(QColor.NameFormat.HexArgb)};
    color: {fg.name()};
    border: none;
    border-radius: 0;
    padding: 0 40px 0 8px;
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 14px;
}}
PasswordBox:disabled {{
    opacity: 0.4;
}}
PasswordBox::placeholder {{
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

        # Bottom accent line
        line_rect = QRectF(
            rect.x(),
            rect.y() + rect.height() - line_width,
            rect.width(),
            line_width,
        )
        painter.fillRect(line_rect, QBrush(line_color))

        # Reveal button
        btn_rect = QRectF(rect.width() - 32, (rect.height() - 20) / 2, 20, 20)
        icon = self._engine.icon(
            FluentIcon.VISIBILITY if not self._revealed else FluentIcon.HIDE,
            color=self._fg, size=16)
        icon.paint(painter, btn_rect.toRect())

        painter.end()

    def mousePressEvent(self, e):
        rect = QRectF(self.rect())
        btn_rect = QRectF(rect.width() - 32, (rect.height() - 20) / 2, 20, 20)
        if btn_rect.contains(e.position()):
            self._revealed = not self._revealed
            self.setEchoMode(
                QLineEdit.EchoMode.Normal if self._revealed else QLineEdit.EchoMode.Password)
            from ...tokens.theme import ThemeManager
            self.on_theme_applied(ThemeManager.instance().theme())
            self.update()
            return
        super().mousePressEvent(e)
