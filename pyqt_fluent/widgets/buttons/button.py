"""Unified Button — 7 styles via ``kind``, overridable colour/radius/icon."""

from __future__ import annotations

from PyQt6.QtCore import QRect, QSize, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPixmap
from PyQt6.QtWidgets import QSizePolicy

from ...tokens.theme import ThemeDefinition
from ...utils.color import derive_accent_variants
from ._base import ButtonBase, _blend


class Button(ButtonBase):
    """Win11 push button — one class for all appearances.

    Parameters
    ----------
    text:
        Label.
    parent:
        Qt parent.
    kind:
        One of ``"standard"``, ``"accent"``, ``"transparent"``, ``"text"``,
        ``"outlined"``, ``"hyperlink"``, ``"filled"``
        (or equivalently ``Button.Kind.*``).
    color:
        Override foreground (text / icon) colour.
    bg_color:
        Override the rest (normal) background fill.
    bg_hover:
        Override the hover background fill.
    bg_pressed:
        Override the pressed background fill.
    radius:
        Override corner radius in pixels.
    icon:
        Path to an icon file drawn to the left of the label.
    """

    class Kind:
        STANDARD = "standard"
        ACCENT = "accent"
        TRANSPARENT = "transparent"
        TEXT = "text"
        OUTLINED = "outlined"
        HYPERLINK = "hyperlink"
        FILLED = "filled"

    _KIND_TOKENS = {
        Kind.STANDARD: (
            "button_standard", "semantic.control_fg",
            "semantic.button_border", "semantic.button_border_accent",
        ),
        Kind.ACCENT: (
            "button_accent", "semantic.on_accent",
            "palette.transparent", "",
        ),
        Kind.TRANSPARENT: (
            "button_transparent", "semantic.control_fg",
            "palette.transparent", "",
        ),
        Kind.TEXT: (
            "button_text", "semantic.accent",
            "palette.transparent", "",
        ),
        Kind.OUTLINED: (
            "button_outlined", "semantic.control_fg",
            "semantic.button_border", "",
        ),
        Kind.HYPERLINK: (
            "button_hyperlink", "semantic.link",
            "palette.transparent", "",
        ),
        Kind.FILLED: (
            "button_filled", "semantic.control_fg",
            "palette.transparent", "",
        ),
    }

    _ICON_GAP = 6

    def __init__(self, text="", parent=None, kind=Kind.STANDARD,
                 color=None, bg_color=None, bg_hover=None,
                 bg_pressed=None, radius=None, icon=None):
        self._my_kind = kind
        (self.control_tokens_key,
         self.fg_ref,
         self.border_ref,
         self.border_accent_ref) = self._KIND_TOKENS[kind]

        self._custom_fg = QColor(color) if color else None
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_bg_hover = QColor(bg_hover) if bg_hover else None
        self._custom_bg_pressed = QColor(bg_pressed) if bg_pressed else None
        self._custom_radius = radius
        self._icon_path = icon
        self._icon_pixmap: QPixmap | None = None

        super().__init__(parent)
        self.setText(text)
        self.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Fixed,
        )

    # ── overrides ────────────────────────────────────────────

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        super().on_theme_applied(theme)

        if self._my_kind == self.Kind.ACCENT:
            accent = self._system_accent()
            if not accent or not accent.isValid():
                r = theme.resolver()
                accent = r.color("semantic.accent")
            variants = derive_accent_variants(accent, theme.is_dark)
            self._bg_rest = variants["rest"]
            self._bg_hover = variants["hover"]
            self._bg_pressed = variants["pressed"]
            self._border = QColor(0, 0, 0, 0)

        if self._my_kind == self.Kind.FILLED:
            self._bg_hover = _blend(self._bg_rest, self._bg_hover)
            self._bg_pressed = _blend(self._bg_rest, self._bg_pressed)

        # User overrides
        if self._custom_fg:
            self._fg = self._custom_fg
        if self._custom_bg:
            self._bg_rest = self._custom_bg
        if self._custom_bg_hover:
            self._bg_hover = self._custom_bg_hover
        if self._custom_bg_pressed:
            self._bg_pressed = self._custom_bg_pressed
        if self._custom_radius is not None:
            self._radius = self._custom_radius

        if self._icon_path:
            self._icon_pixmap = QPixmap(self._icon_path)
            if self._icon_pixmap.isNull():
                self._icon_pixmap = None

    @staticmethod
    def _system_accent():
        try:
            from ...utils.win32_utils import get_system_accent_color
            return get_system_accent_color()
        except Exception:
            return None

    def _draw_indicator(self, painter: QPainter) -> None:
        self._draw_background(painter)
        painter.setPen(self._fg)
        f = QFont()
        f.setPixelSize(14)
        painter.setFont(f)

        r = self.rect()
        if self._icon_pixmap:
            sz = min(r.height(), 18)
            pix = self._icon_pixmap.scaled(
                sz, sz, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            ix = r.x() + (r.width() - self._text_width() - self._ICON_GAP - sz) // 2
            iy = r.y() + (r.height() - sz) // 2
            painter.drawPixmap(ix, iy, pix)
            text_rect = QRect(ix + sz + self._ICON_GAP, r.y(),
                              r.width() - (ix + sz + self._ICON_GAP - r.x()), r.height())
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                             self.text())
        else:
            painter.drawText(r, Qt.AlignmentFlag.AlignCenter, self.text())

    def _text_width(self) -> int:
        from PyQt6.QtGui import QFontMetrics
        return QFontMetrics(self.font()).horizontalAdvance(self.text().replace("&", ""))

    def sizeHint(self):
        base = super().sizeHint()
        if self._icon_pixmap:
            return QSize(base.width() + 18 + self._ICON_GAP, base.height())
        return base


# ── ToggleButton (separate class) ───────────────────────────


class ToggleButton(Button):
    """Checkable push button — toggles between subtle-fill and accent-fill."""

    def __init__(self, text="", parent=None, kind=Button.Kind.STANDARD,
                 color=None, bg_color=None, bg_hover=None,
                 bg_pressed=None, radius=None, icon=None):
        super().__init__(text, parent, kind=kind,
                         color=color, bg_color=bg_color,
                         bg_hover=bg_hover, bg_pressed=bg_pressed,
                         radius=radius, icon=icon)
        self.setCheckable(True)

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        super().on_theme_applied(theme)
        r = theme.resolver()
        self._bg_pressed = r.color("semantic.accent_pressed")
        if self.isChecked():
            self._bg_rest = r.color("semantic.accent")
            self._bg_hover = r.color("semantic.accent_hover")
            self._fg = r.color("semantic.on_accent")
        else:
            self._bg_rest = r.color("semantic.subtle_fill")
            self._bg_hover = r.color("semantic.hover")
            self._fg = r.color("semantic.control_fg")

    def nextCheckState(self):
        super().nextCheckState()
        from ...tokens.theme import ThemeManager
        self.on_theme_applied(ThemeManager.instance().theme())
        self._start_bg_animation()


# ── legacy aliases ──────────────────────────────────────────


class PushButton(Button):
    """Legacy alias — use ``Button(kind=Button.Kind.STANDARD)``."""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent, kind=Button.Kind.STANDARD)


class AccentButton(Button):
    """Legacy alias — use ``Button(kind=Button.Kind.ACCENT)``."""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent, kind=Button.Kind.ACCENT)


class TransparentButton(Button):
    """Legacy alias — use ``Button(kind=Button.Kind.TRANSPARENT)``."""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent, kind=Button.Kind.TRANSPARENT)


class TextButton(Button):
    """Legacy alias — use ``Button(kind=Button.Kind.TEXT)``."""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent, kind=Button.Kind.TEXT)


class OutlinedButton(Button):
    """Legacy alias — use ``Button(kind=Button.Kind.OUTLINED)``."""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent, kind=Button.Kind.OUTLINED)


class HyperlinkButton(Button):
    """Legacy alias — use ``Button(kind=Button.Kind.HYPERLINK)``."""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent, kind=Button.Kind.HYPERLINK)


class FilledButton(Button):
    """Legacy alias — use ``Button(kind=Button.Kind.FILLED)``."""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent, kind=Button.Kind.FILLED)
