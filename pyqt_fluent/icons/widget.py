"""IconWidget — theme-aware SVG icon widget using the centralized IconEngine."""

from __future__ import annotations

from PyQt6.QtCore import QRectF, QSize, Qt
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QSizePolicy, QWidget

from ..tokens.theme import ThemeDefinition
from ..widgets._shared.theme_aware import ThemeAwareWidget
from .engine import FluentIcon, IconEngine


class IconWidget(ThemeAwareWidget, QWidget):
    """SVG icon that auto-colours from a theme token.

    Parameters
    ----------
    icon_name:
        ``FluentIcon`` member or icon file name (without ``.svg``).
    color_ref:
        Theme token path for the icon foreground colour.
    fill_ref:
        Optional theme token path for fill colour.
    size:
        Logical icon size in pixels.
    opacity:
        Painter opacity (0.0 – 1.0).
    parent:
        Qt parent widget.
    """

    def __init__(
        self,
        icon_name: str | FluentIcon = "",
        color_ref: str = "semantic.control_fg",
        fill_ref: str = "",
        size: int = 16,
        opacity: float = 1.0,
        parent=None,
    ):
        super().__init__(parent)
        self._icon_name: str | FluentIcon = icon_name
        self._color_ref = color_ref
        self._fill_ref = fill_ref
        self._color = QColor()
        self._fill = QColor()
        self._size = size
        self._opacity = opacity
        self._engine = IconEngine.instance()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(QSize(size, size))
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self._init_theme_aware()

    # ── public API ──────────────────────────────────────────

    def set_icon(self, name: str | FluentIcon) -> None:
        """Set the icon name (FluentIcon enum or string without .svg)."""
        self._icon_name = name
        self.update()

    def set_color_ref(self, ref: str) -> None:
        """Set the theme token path for the icon colour."""
        self._color_ref = ref
        from ..tokens.theme import ThemeManager

        self._apply_theme(ThemeManager.instance().theme())

    def set_fill_ref(self, ref: str) -> None:
        """Set the theme token path for the fill colour."""
        self._fill_ref = ref
        from ..tokens.theme import ThemeManager

        self._apply_theme(ThemeManager.instance().theme())

    def set_icon_size(self, size: int) -> None:
        """Set the logical icon size."""
        self._size = size
        self.setFixedSize(QSize(size, size))
        self.update()

    def set_opacity(self, opacity: float) -> None:
        """Set the painter opacity."""
        self._opacity = opacity
        self.update()

    # ── theme ───────────────────────────────────────────────

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._color = r.color(self._color_ref)
        if self._fill_ref:
            self._fill = r.color(self._fill_ref)
        self.update()

    # ── paint ───────────────────────────────────────────────

    def paintEvent(self, e) -> None:
        if not self._icon_name:
            return
        painter = QPainter(self)
        fill = self._fill if self._fill_ref else None
        self._engine.render(
            painter,
            QRectF(self.rect()),
            self._icon_name,
            color=self._color,
            fill_color=fill,
            opacity=self._opacity,
        )
        painter.end()
