"""Stylesheet engine that builds QSS from design tokens.

The engine resolves token expressions like ``{{component.window_bg}}``
into QSS-compatible values (hex colours, ``px`` lengths, etc.).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from PyQt6.QtGui import QColor

from ..tokens.resolver import TokenResolver
from ..tokens.typography import Typography


@dataclass
class StylesheetEngine:
    """Generates and memoïzes QSS per widget type.

    Usage::

        engine = StylesheetEngine(resolver, typography)
        engine.register("QPushButton", "background: {{component.button_primary.rest}}; ...")
        qss = engine.generate("QPushButton")
    """

    resolver: TokenResolver
    typography: Typography
    _custom: dict[str, str] = field(default_factory=dict, repr=False)
    _cache: dict[str, str] = field(default_factory=dict, repr=False)

    # --- public API ---

    def register(self, widget_type: str, rule: str) -> None:
        """Register a custom QSS *rule* for a *widget_type*."""
        self._custom[widget_type] = rule
        self._cache.pop(widget_type, None)

    def unregister(self, widget_type: str) -> None:
        """Remove a previously registered custom rule."""
        self._custom.pop(widget_type, None)
        self._cache.pop(widget_type, None)

    def generate(self, widget_type: str) -> str:
        """Return QSS for *widget_type*, using registered rule > built-in > base."""
        if widget_type in self._cache:
            return self._cache[widget_type]

        # 1. Registered custom rule
        if widget_type in self._custom:
            raw = self._custom[widget_type]
            qss = self._interpolate(raw)
            self._cache[widget_type] = qss
            return qss

        # 2. Built-in rule
        built = _BUILT_INS.get(widget_type)
        if built is not None:
            qss = self._interpolate(built)
            self._cache[widget_type] = qss
            return qss

        # 3. Minimal base fallback
        qss = self._base_qss()
        self._cache[widget_type] = qss
        return qss

    # --- internal ---

    @staticmethod
    def _fmt(value: object) -> str:
        """Convert a resolved token value into a CSS fragment."""
        if isinstance(value, QColor):
            return value.name()
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)

    def _interpolate(self, rule: str) -> str:
        """Replace ``{{token.path}}`` with resolved CSS values."""

        def repl(match: re.Match[str]) -> str:
            token = match.group(1).strip()
            # typography.* is handled separately
            if token.startswith("typography."):
                return self._resolve_typography(token)
            try:
                val = self.resolver.resolve(token)
                return self._fmt(val)
            except (KeyError, TypeError, AttributeError):
                return match.group(0)

        return re.sub(r"\{\{\s*(.+?)\s*\}\}", repl, rule)

    def _resolve_typography(self, token: str) -> str:
        """Resolve a ``typography.property`` token."""
        # e.g. typography.fontFamily or typography.body.size
        parts = token.split(".")
        if len(parts) == 2 and parts[1] == "fontFamily":
            return self.typography.fontFamily
        if len(parts) == 2 and parts[1] == "fallbackFamilies":
            return ", ".join(self.typography.fallbackFamilies)
        if len(parts) == 2:
            # e.g. typography.body -> size/weight as "14px"
            ramp = getattr(self.typography, parts[1], None)
            if ramp is not None:
                return f"{ramp.size}px"
        if len(parts) == 3 and parts[2] == "weight":
            ramp = getattr(self.typography, parts[1], None)
            if ramp is not None:
                return str(ramp.weight.value)
        return ""

    def _base_qss(self) -> str:
        """Minimal base QSS that only sets font and global bg/fg."""
        r = self.resolver
        try:
            bg = r.color("component.window_bg").name()
            fg = r.color("component.window_fg").name()
            ff = self.typography.fontFamily
            base = self.typography.body.size
        except (KeyError, TypeError):
            bg = "#FFFFFF"
            fg = "#000000"
            ff = "Segoe UI"
            base = 14
        return f"""
        QWidget {{
            background-color: {bg};
            color: {fg};
            font-family: "{ff}";
            font-size: {base}px;
        }}
        """

    # --- convenience: batch ---

    def stylesheets(self, *widget_types: str) -> dict[str, str]:
        """Generate QSS for many widget types at once."""
        return {wt: self.generate(wt) for wt in widget_types}

    # --- one-shot from theme (for ThemeAwareWidget) ---

    @classmethod
    def for_role(cls, role: str, theme: ThemeDefinition) -> str:
        """Build QSS for a *role* string from a ``ThemeDefinition``.

        ``role`` can be any key registered in ``_BUILT_INS`` (e.g. ``"QPushButton"``)
        or previously registered via ``register()``.
        """
        r = theme.resolver()
        engine = cls(r, theme.typography)
        return engine.generate(role)


_BUILT_INS: dict[str, str] = {
    "QWidget": "", # Base has enough
    "QLabel": """QLabel { background: transparent; color: {{component.content_fg}}; }""",
    "QPushButton": """
    QPushButton {
        background-color: {{component.button_primary.rest}};
        color: {{component.button_primary_fg}};
        border: {{component.border_width}}px solid {{component.border}};
        border-radius: {{component.control_radius}}px;
        padding: {{component.button_padding_vertical}}px {{component.button_padding_horizontal}}px;
        min-height: {{component.button_height}}px;
    }
    QPushButton:hover { background-color: {{component.button_primary.hover}}; }
    QPushButton:pressed { background-color: {{component.button_primary.pressed}}; }
    QPushButton:disabled { opacity: {{component.disabled_opacity}}; }
    QPushButton:focus {
        outline: none;
        border: 1px solid {{semantic.focus_ring}};
    }
    """,
    "FluentButton": """
    FluentButton {
        background-color: {{component.button_primary.rest}};
        color: {{component.button_primary_fg}};
        border: none;
        border-radius: {{component.control_radius}}px;
        padding: {{component.button_padding_vertical}}px {{component.button_padding_horizontal}}px;
        min-height: {{component.button_height}}px;
    }
    FluentButton:hover { background-color: {{component.button_primary.hover}}; }
    FluentButton:pressed { background-color: {{component.button_primary.pressed}}; }
    FluentButton:disabled { opacity: {{component.disabled_opacity}}; }
    """,
    "QLineEdit": """
    QLineEdit {
        background-color: {{component.input_bg}};
        color: {{component.input_fg}};
        border: {{component.border_width}}px solid {{component.input_border}};
        border-radius: {{component.control_radius}}px;
        padding: {{component.input_padding_vertical}}px {{component.input_padding_horizontal}}px;
        min-height: {{component.input_height}}px;
    }
    QLineEdit:focus {
        border-color: {{component.input_focus_border}};
        outline: none;
    }
    QLineEdit:disabled { opacity: {{component.disabled_opacity}}; }
    """,
    "QTextEdit": """
    QTextEdit {
        background-color: {{component.input_bg}};
        color: {{component.content_fg}};
        border: {{component.border_width}}px solid {{component.input_border}};
        border-radius: {{component.control_radius}}px;
        padding: {{component.input_padding_vertical}}px {{component.input_padding_horizontal}}px;
    }
    QTextEdit:focus {
        border-color: {{component.input_focus_border}};
        outline: none;
    }
    QTextEdit:disabled { opacity: {{component.disabled_opacity}}; }
    """,
    "QPlainTextEdit": """
    QPlainTextEdit {
        background-color: {{component.input_bg}};
        color: {{component.content_fg}};
        border: {{component.border_width}}px solid {{component.input_border}};
        border-radius: {{component.control_radius}}px;
        padding: {{component.input_padding_vertical}}px {{component.input_padding_horizontal}}px;
    }
    QPlainTextEdit:focus {
        border-color: {{component.input_focus_border}};
        outline: none;
    }
    QPlainTextEdit:disabled { opacity: {{component.disabled_opacity}}; }
    """,
    "QComboBox": """
    QComboBox {
        background-color: {{component.input_bg}};
        color: {{component.content_fg}};
        border: {{component.border_width}}px solid {{component.input_border}};
        border-radius: {{component.control_radius}}px;
        padding: {{component.input_padding_vertical}}px {{component.input_padding_horizontal}}px;
        min-height: {{component.input_height}}px;
    }
    QComboBox:focus {
        border-color: {{component.input_focus_border}};
        outline: none;
    }
    QComboBox:disabled { opacity: {{component.disabled_opacity}}; }
    QComboBox::drop-down {
        border: none;
        background: transparent;
        padding-right: 12px;
    }
    QComboBox::down-arrow {
        width: 12px;
        height: 12px;
    }
    """,
    "QCheckBox": """
    QCheckBox {
        color: {{component.content_fg}};
        spacing: 8px;
    }
    QCheckBox:disabled { opacity: {{component.disabled_opacity}}; }
    QCheckBox::indicator {
        width: {{component.checkbox_size}}px;
        height: {{component.checkbox_size}}px;
        border: {{component.border_width}}px solid {{component.input_border}};
        border-radius: {{component.control_radius}}px;
        background-color: {{component.input_bg}};
    }
    QCheckBox::indicator:checked {
        background-color: {{semantic.accent}};
        border-color: {{semantic.accent}};
    }
    QCheckBox::indicator:hover {
        border-color: {{semantic.accent_hover}};
    }
    QCheckBox::indicator:disabled { opacity: {{component.disabled_opacity}}; }
    """,
    "QRadioButton": """
    QRadioButton {
        color: {{component.content_fg}};
        spacing: 8px;
    }
    QRadioButton:disabled { opacity: {{component.disabled_opacity}}; }
    QRadioButton::indicator {
        width: {{component.radio_button_size}}px;
        height: {{component.radio_button_size}}px;
        border: {{component.border_width}}px solid {{component.input_border}};
        border-radius: 50%;
        background-color: {{component.input_bg}};
    }
    QRadioButton::indicator:checked {
        background-color: {{semantic.accent}};
        border-color: {{semantic.accent}};
    }
    QRadioButton::indicator:hover {
        border-color: {{semantic.accent_hover}};
    }
    QRadioButton::indicator:disabled { opacity: {{component.disabled_opacity}}; }
    """,
    "QSlider": """
    QSlider::groove:horizontal {
        border: none;
        height: {{component.slider_height}}px;
        background: {{component.border}};
        border-radius: 2px;
    }
    QSlider::handle:horizontal {
        background: {{semantic.accent}};
        border: none;
        width: {{component.slider_handle_size}}px;
        height: {{component.slider_handle_size}}px;
        margin: -{{component.slider_handle_size // 2}}px 0;
        border-radius: 50%;
    }
    QSlider::groove:vertical {
        border: none;
        width: {{component.slider_height}}px;
        background: {{component.border}};
        border-radius: 2px;
    }
    QSlider::handle:vertical {
        background: {{semantic.accent}};
        border: none;
        width: {{component.slider_handle_size}}px;
        height: {{component.slider_handle_size}}px;
        margin: 0 -{{component.slider_handle_size // 2}}px;
        border-radius: 50%;
    }
    QSlider:disabled { opacity: {{component.disabled_opacity}}; }
    """,
    "QScrollBar": """
    QScrollBar:vertical {
        background: {{component.scrollbar_bg}};
        width: {{component.scrollbar_width}}px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background: {{component.scrollbar_fg}};
        border-radius: 4px;
        min-height: {{component.scrollbar_handle_min_size}}px;
    }
    QScrollBar::handle:vertical:hover { background: {{semantic.accent_hover}}; }
    QScrollBar::handle:vertical:pressed { background: {{semantic.accent}}; }
    QScrollBar:horizontal {
        background: {{component.scrollbar_bg}};
        height: {{component.scrollbar_width}}px;
        border-radius: 4px;
    }
    QScrollBar::handle:horizontal {
        background: {{component.scrollbar_fg}};
        border-radius: 4px;
        min-width: {{component.scrollbar_handle_min_size}}px;
    }
    QScrollBar::handle:horizontal:hover { background: {{semantic.accent_hover}}; }
    QScrollBar::handle:horizontal:pressed { background: {{semantic.accent}}; }
    QScrollBar:disabled { opacity: {{component.disabled_opacity}}; }
    """,
    "QGroupBox": """
    QGroupBox {
        color: {{component.content_fg}};
        border: {{component.border_width}}px solid {{component.border}};
        border-radius: {{component.control_radius}}px;
        margin-top: 8px;
        padding-top: 12px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 2px;
        color: {{component.content_fg}};
    }
    """,
    "QToolTip": """
    QToolTip {
        background-color: {{component.content_bg}};
        color: {{component.content_fg}};
        border: {{component.border_width}}px solid {{component.border}};
        border-radius: {{component.control_radius}}px;
        padding: 6px 10px;
        font-size: {{typography.caption.size}}px;
    }
    """,
    "QProgressBar": """
    QProgressBar {
        border: {{component.border_width}}px solid {{component.border}};
        border-radius: {{component.control_radius}}px;
        background: {{component.input_bg}};
        text-align: center;
    }
    QProgressBar::chunk {
        background: {{semantic.accent}};
        border-radius: {{component.control_radius}}px;
    }
    QProgressBar:disabled { opacity: {{component.disabled_opacity}}; }
    """,
    "QSpinBox": """
    QSpinBox {
        background-color: {{component.input_bg}};
        color: {{component.content_fg}};
        border: {{component.border_width}}px solid {{component.input_border}};
        border-radius: {{component.control_radius}}px;
        padding: {{component.input_padding_vertical}}px {{component.input_padding_horizontal}}px;
        min-height: {{component.input_height}}px;
    }
    QSpinBox:focus {
        border-color: {{component.input_focus_border}};
        outline: none;
    }
    QSpinBox:disabled { opacity: {{component.disabled_opacity}}; }
    QSpinBox::up-button, QSpinBox::down-button {
        border: none;
        background: transparent;
        width: 20px;
    }
    QSpinBox::up-arrow, QSpinBox::down-arrow {
        width: 12px;
        height: 12px;
    }
    """,
}
