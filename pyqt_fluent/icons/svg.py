"""SvgIcon — lightweight value object for theme-aware SVG icon rendering."""

from __future__ import annotations

from dataclasses import dataclass, field

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor, QIcon, QPainter, QPixmap

from .engine import FluentIcon, IconEngine


@dataclass
class SvgIcon:
    """Lightweight SVG icon descriptor for rendering in paintEvent.

    Parameters
    ----------
    icon:
        Built-in ``FluentIcon`` enum member or a custom icon name string.
    color:
        Stroke / foreground colour. Falls back to theme ``semantic.control_fg``.
    fill_color:
        Optional fill colour (for icons with ``currentColor`` fill).
    size:
        Logical size in pixels (used when rendering to QIcon/QPixmap).
    opacity:
        Painter opacity (0.0 – 1.0).

    Usage::

        def paintEvent(self, e):
            painter = QPainter(self)
            icon = SvgIcon(FluentIcon.CLOSE, color=QColor("red"))
            icon.render(painter, QRectF(self.rect()))
    """

    icon: str | FluentIcon = FluentIcon.CHECKMARK
    color: QColor = field(default_factory=lambda: QColor(0, 0, 0))
    fill_color: QColor | None = None
    size: int = 16
    opacity: float = 1.0

    def render(self, painter: QPainter, rect: QRectF) -> None:
        """Render the icon into *rect* using the centralized IconEngine."""
        IconEngine.instance().render(
            painter,
            rect,
            self.icon,
            color=self.color,
            fill_color=self.fill_color,
            opacity=self.opacity,
        )

    def to_qicon(self) -> QIcon:
        """Convert to QIcon for use in QAction / QPushButton."""
        return IconEngine.instance().icon(
            self.icon,
            color=self.color,
            fill_color=self.fill_color,
            size=self.size,
        )

    def to_pixmap(self) -> QPixmap:
        """Convert to QPixmap for direct painting."""
        return IconEngine.instance().pixmap(
            self.icon,
            color=self.color,
            fill_color=self.fill_color,
            size=self.size,
        )

    def with_color(self, color: QColor) -> SvgIcon:
        """Return a copy with a different colour."""
        return SvgIcon(
            icon=self.icon,
            color=color,
            fill_color=self.fill_color,
            size=self.size,
            opacity=self.opacity,
        )

    def with_size(self, size: int) -> SvgIcon:
        """Return a copy with a different size."""
        return SvgIcon(
            icon=self.icon,
            color=self.color,
            fill_color=self.fill_color,
            size=size,
            opacity=self.opacity,
        )

    def with_opacity(self, opacity: float) -> SvgIcon:
        """Return a copy with a different opacity."""
        return SvgIcon(
            icon=self.icon,
            color=self.color,
            fill_color=self.fill_color,
            size=self.size,
            opacity=opacity,
        )
