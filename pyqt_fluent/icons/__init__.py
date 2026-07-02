"""Centralized icon management — theme-aware SVG rendering with caching.

Usage::

    from pyqt_fluent.icons import FluentIcon, IconEngine, SvgIcon, IconWidget

    # Get a QIcon for use in QAction / QPushButton
    icon = IconEngine.icon(FluentIcon.CHECKMARK, color=QColor("blue"))

    # Render directly in paintEvent
    SvgIcon(FluentIcon.CLOSE, color=fg).render(painter, rect)

    # Use as a standalone widget
    widget = IconWidget(icon_name=FluentIcon.SEARCH, size=20)
"""

from .engine import FluentIcon, IconEngine  # noqa: F401
from .svg import SvgIcon  # noqa: F401
from .widget import IconWidget  # noqa: F401
