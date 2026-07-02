"""IconEngine — centralized SVG icon loading, caching, and theme-aware rendering.

The engine loads SVGs from ``pyqt_fluent.resources/icons/``, caches parsed
``QDomDocument`` + raw ``QByteArray`` per icon name, and provides methods
to render them with custom colours, sizes, and opacity.
"""

from __future__ import annotations

import re
from enum import Enum
from importlib.resources import files as _resources

from PyQt6.QtCore import QByteArray, QRectF
from PyQt6.QtGui import QColor, QIcon, QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtXml import QDomDocument


class FluentIcon(Enum):
    """Built-in Fluent UI icon names."""

    ADD_CIRCLE = "AddCircle_filled"
    ADD_SQUARE = "AddSquare_filled"
    ALERT = "Alert_filled"
    ARROW_DOWN = "ArrowDown_filled"
    ARROW_LEFT = "ArrowLeft_filled"
    ARROW_REDO = "ArrowRedo_filled"
    ARROW_RIGHT = "ArrowRight_filled"
    ARROW_UNDO = "ArrowUndo_filled"
    ARROW_UP = "ArrowUp_filled"
    CARET_DOWN = "CaretDown_filled"
    CARET_LEFT = "CaretLeft_filled"
    CARET_RIGHT = "CaretRight_filled"
    CARET_UP = "CaretUp_filled"
    CHECKBOX_CHECKED = "CheckboxChecked_filled"
    CHECKBOX_INDETERMINATE = "CheckboxIndeterminate_filled"
    CHECKBOX_UNCHECKED = "CheckboxUnchecked_filled"
    CHECKMARK = "Checkmark"
    CHECKMARK_CIRCLE = "CheckmarkCircle_filled"
    CHEVRON_DOWN = "ChevronDown_filled"
    CHEVRON_LEFT = "ChevronLeft_filled"
    CHEVRON_RIGHT = "ChevronRight_filled"
    CHEVRON_UP = "ChevronUp_filled"
    CLOSE = "close"
    DISMISS = "Dismiss_filled"
    DOWNLOAD = "Download_filled"
    HOME = "Home_filled"
    INFO = "Info_filled"
    LINE_HORIZONTAL_3 = "LineHorizontal3_filled"
    NEW = "New_filled"
    OPEN = "Open_filled"
    RADIO_BUTTON_FILLED = "RadioButton_filled"
    RADIO_BUTTON_OUTLINED = "RadioButton_outlined"
    SAVE = "Save_filled"
    SEARCH = "Search_filled"
    SETTINGS = "Settings_filled"
    STATUS = "Status_filled"
    WARNING = "Warning_filled"
    WEATHER_MOON = "WeatherMoon_filled"
    WEATHER_SUNNY = "WeatherSunny_filled"
    VISIBILITY = "Eye_filled"
    HIDE = "EyeOff_filled"
    DELETE = "Delete_filled"
    EDIT = "Edit_filled"
    SORT = "Sort_filled"


def _svg_color_str(c: QColor) -> str:
    """Convert QColor to SVG color string (hex format for best SVG compat)."""
    return c.name()


class _IconCacheEntry:
    """Cached parsed SVG data."""

    __slots__ = ("raw", "dom")

    def __init__(self, raw: QByteArray, dom: QDomDocument):
        self.raw = raw
        self.dom = dom


# ── Regex patterns for SVG string-level recoloring ─────────────

_RE_STYLE_BLOCK = re.compile(r"<style[^>]*>.*?</style>", re.DOTALL | re.IGNORECASE)

_RE_FILL_ATTR = re.compile(r"""\bfill\s*=\s*(["'])([^"']*?)\1""", re.IGNORECASE)

_RE_STROKE_ATTR = re.compile(r"""\bstroke\s*=\s*(["'])([^"']*?)\1""", re.IGNORECASE)

_RE_STYLE_FILL = re.compile(r"""\bfill\s*:\s*([^;"'>]+)""", re.IGNORECASE)

_RE_STYLE_STROKE = re.compile(r"""\bstroke\s*:\s*([^;"'>]+)""", re.IGNORECASE)

# Shape tags whose colour may have come from a <style> block that we stripped.
_RE_SHAPE_TAG = re.compile(
    r"""<(path|circle|rect|polygon|ellipse|line|polyline)(\s[^>]*?)/?\s*>""",
    re.DOTALL | re.IGNORECASE,
)


def _replace_fill_attr(m: re.Match, color_str: str) -> str:
    """Replace ``fill`` with the target colour for ``currentColor`` and ``none``;
    leave hardcoded colours (``#ffffff``, ``rgba(...)``, etc.) alone."""
    quote = m.group(1)
    value = m.group(2).strip()
    if value.lower() in ("currentcolor", "none"):
        return f"fill={quote}{color_str}{quote}"
    return m.group(0)


def _replace_stroke_attr(m: re.Match, color_str: str) -> str:
    """Replace stroke attribute value unless it is 'none'."""
    quote = m.group(1)
    value = m.group(2).strip()
    if value.lower() == "none":
        return m.group(0)
    return f"stroke={quote}{color_str}{quote}"


def _replace_style_fill(m: re.Match, color_str: str) -> str:
    """Replace inline ``fill`` value for ``currentColor`` and ``none``."""
    value = m.group(1).strip()
    if value.lower() in ("currentcolor", "none"):
        return f"fill:{color_str}"
    return m.group(0)


def _replace_style_stroke(m: re.Match, color_str: str) -> str:
    """Replace stroke inside an inline style unless it is 'none'."""
    value = m.group(1).strip()
    if value.lower() == "none":
        return m.group(0)
    return f"stroke:{color_str}"


def _inject_fill_if_missing(svg: str, fill_str: str) -> str:
    """Add ``fill="<fill_str>"`` to shape tags that have no ``fill=""`` attribute.

    After ``<style>`` blocks are stripped, shapes whose colour was set via a CSS
    class (e.g. ``class="cls-1"``) end up with no fill at all, defaulting to
    black.  This function catches them.
    """

    def _inject(m: re.Match) -> str:
        tag = m.group(1)
        attrs = m.group(2)
        if "fill=" not in attrs:
            raw = m.group(0)
            if raw.rstrip().endswith("/>"):
                return f"<{tag}{attrs} fill=\"{fill_str}\" />"
            else:
                return f"<{tag}{attrs} fill=\"{fill_str}\">"
        return m.group(0)

    return _RE_SHAPE_TAG.sub(_inject, svg)


class IconEngine:
    """Singleton that manages SVG icon loading, caching, and rendering.

    Usage::

        engine = IconEngine.instance()

        # Get a QIcon
        icon = engine.icon(FluentIcon.CLOSE, color=QColor("red"), size=16)

        # Render directly
        engine.render(painter, rect, FluentIcon.CLOSE, color=fg)

        # Load from file path
        engine.render(painter, rect, "/path/to/icon.svg", color=fg)

    """

    _instance: IconEngine | None = None

    def __init__(self):
        self._cache: dict[str, _IconCacheEntry] = {}
        self._renderer_cache: dict[str, QSvgRenderer] = {}

    @classmethod
    def instance(cls) -> IconEngine:
        if cls._instance is None:
            cls._instance = IconEngine()
        return cls._instance

    # ── path resolution ─────────────────────────────────────────

    def resolve_path(self, icon: str | FluentIcon) -> str:
        """Resolve an icon name to a file path."""
        if isinstance(icon, FluentIcon):
            name = icon.value
        else:
            name = icon
        p = _resources("pyqt_fluent.resources").joinpath("icons", f"{name}.svg")
        return str(p)

    # ── loading ─────────────────────────────────────────────────

    def _load(self, icon: str | FluentIcon) -> _IconCacheEntry:
        """Load and cache SVG data for an icon."""
        key = icon.value if isinstance(icon, FluentIcon) else icon
        if key in self._cache:
            return self._cache[key]

        raw = QByteArray()
        try:
            # ✅ Read bytes directly from the package resources
            ref = _resources("pyqt_fluent.resources").joinpath("icons", f"{key}.svg")
            raw_bytes = ref.read_bytes()
            raw = QByteArray(raw_bytes)
        except (FileNotFoundError, TypeError) as e:
            # 🛡️ Now it will print a warning instead of failing silently!
            print(f"[IconEngine] WARNING: Icon '{key}' not found or unreadable. ({e})")

        dom = QDomDocument()
        dom.setContent(raw)
        entry = _IconCacheEntry(raw, dom)
        self._cache[key] = entry
        return entry

    # ── recoloring ──────────────────────────────────────────────

    def _recolor_svg_string(
        self,
        raw_bytes: bytes,
        color: QColor,
        fill_color: QColor | None = None,
    ) -> QByteArray:
        """Recolor SVG by operating on the raw XML string.

        This is more robust than DOM-level manipulation because:
        - It handles ``<style>`` blocks (CSS overrides) by stripping them
        - It overrides *all* fill/stroke values, not only ``currentColor`` / empty
        - It preserves the original SVG structure faithfully
        """
        target = fill_color if fill_color is not None else color
        fill_str = _svg_color_str(target)
        stroke_str = _svg_color_str(color)

        try:
            svg = raw_bytes.decode("utf-8", errors="replace")
        except Exception:
            svg = raw_bytes.data().decode("utf-8", errors="replace")

        # 1. Strip <style> blocks — they have higher CSS specificity than
        #    presentation attributes and would override our fill/stroke.
        svg = _RE_STYLE_BLOCK.sub("", svg)

        # 2. Override fill="currentColor" with the target color
        svg = _RE_FILL_ATTR.sub(lambda m: _replace_fill_attr(m, fill_str), svg)

        # 3. Override stroke attributes on every element (except stroke="none")
        svg = _RE_STROKE_ATTR.sub(lambda m: _replace_stroke_attr(m, stroke_str), svg)

        # 4. Override fill:currentColor inside inline style=""
        svg = _RE_STYLE_FILL.sub(lambda m: _replace_style_fill(m, fill_str), svg)

        # 5. Override stroke inside inline style="" (except stroke:none)
        svg = _RE_STYLE_STROKE.sub(lambda m: _replace_style_stroke(m, stroke_str), svg)

        # 6. Inject fill on shape tags that lost their colour source when
        #    <style> was stripped (CSS-class-based colouring).
        svg = _inject_fill_if_missing(svg, fill_str)

        return QByteArray(svg.encode("utf-8"))

    def _recolor_dom(
        self,
        dom: QDomDocument,
        color: QColor,
        fill_color: QColor | None = None,
    ) -> QByteArray:
        """Clone DOM and apply colour to stroke/fill attributes.

        Uses string-level recoloring for maximum compatibility with SVGs
        that use CSS ``<style>`` blocks or explicit fill colours.
        """
        raw_bytes = dom.toByteArray().data()
        return self._recolor_svg_string(raw_bytes, color, fill_color)

    # ── rendering ───────────────────────────────────────────────

    def render(
        self,
        painter: QPainter,
        rect: QRectF,
        icon: str | FluentIcon,
        color: QColor | None = None,
        fill_color: QColor | None = None,
        opacity: float = 1.0,
    ) -> None:
        """Render an SVG icon into *rect* with optional recoloring."""
        entry = self._load(icon)
        if entry.raw.isEmpty():
            return

        color = color or QColor(0, 0, 0)
        colored_data = self._recolor_svg_string(bytes(entry.raw.data()), color, fill_color)

        renderer = QSvgRenderer(colored_data)
        if not renderer.isValid():
            return

        painter.save()
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform
        )
        painter.setOpacity(opacity)
        renderer.render(painter, rect)
        painter.restore()

    def icon(
        self,
        icon: str | FluentIcon,
        color: QColor | None = None,
        fill_color: QColor | None = None,
        size: int = 16,
    ) -> QIcon:
        """Return a QIcon for use in QAction, QPushButton, etc."""
        entry = self._load(icon)
        if entry.raw.isEmpty():
            return QIcon()

        color = color or QColor(0, 0, 0)
        colored_data = self._recolor_svg_string(bytes(entry.raw.data()), color, fill_color)

        pix = QPixmap(size, size)
        pix.fill(QColor(0, 0, 0, 0))
        renderer = QSvgRenderer(colored_data)
        if not renderer.isValid():
            return QIcon()
        painter = QPainter(pix)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform
        )
        renderer.render(painter, QRectF(pix.rect()))
        painter.end()
        return QIcon(pix)

    def pixmap(
        self,
        icon: str | FluentIcon,
        color: QColor | None = None,
        fill_color: QColor | None = None,
        size: int = 16,
    ) -> QPixmap:
        """Return a QPixmap for direct painting."""
        entry = self._load(icon)
        if entry.raw.isEmpty():
            return QPixmap()

        color = color or QColor(0, 0, 0)
        colored_data = self._recolor_svg_string(bytes(entry.raw.data()), color, fill_color)

        pix = QPixmap(size, size)
        pix.fill(QColor(0, 0, 0, 0))
        renderer = QSvgRenderer(colored_data)
        if not renderer.isValid():
            return QPixmap()
        painter = QPainter(pix)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform
        )
        renderer.render(painter, QRectF(pix.rect()))
        painter.end()
        return pix

    def clear_cache(self) -> None:
        """Clear all cached SVG data."""
        self._cache.clear()
        self._renderer_cache.clear()
