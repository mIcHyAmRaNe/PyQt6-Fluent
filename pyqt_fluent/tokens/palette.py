"""Palier 1 — Primitives. Raw colours with no semantic meaning."""

from __future__ import annotations

from dataclasses import dataclass, field

from PyQt6.QtGui import QColor


@dataclass(frozen=True)
class PaletteToken:
    name: str
    light: QColor
    dark: QColor

    def for_mode(self, is_dark: bool) -> QColor:
        return self.dark if is_dark else self.light

    def hex(self, is_dark: bool) -> str:
        return self.for_mode(is_dark).name()


@dataclass
class PaletteFamily:
    _data: dict = field(default_factory=dict, repr=False)

    @classmethod
    def with_values(cls, **kw: PaletteToken) -> PaletteFamily:
        return cls(_data={k: v for k, v in kw.items()})

    def __getattr__(self, key: str) -> PaletteToken:
        try:
            return self._data[key]
        except KeyError:
            raise AttributeError(key)

    def __getitem__(self, idx: int) -> PaletteToken:
        return self._data[str(idx)]


def _scale(hex_light: str, hex_dark: str, name: str) -> PaletteToken:
    return PaletteToken(name, QColor(hex_light), QColor(hex_dark))


@dataclass
class Palette:
    gray: PaletteFamily = field(default_factory=lambda: PaletteFamily.with_values(
        **{"50": _scale("#F9FAFB", "#F9FAFB", "gray.50"),
           "100": _scale("#F3F4F6", "#F3F4F6", "gray.100"),
           "200": _scale("#E5E7EB", "#E5E7EB", "gray.200"),
           "300": _scale("#D1D5DB", "#D1D5DB", "gray.300"),
           "400": _scale("#9CA3AF", "#9CA3AF", "gray.400"),
           "500": _scale("#6B7280", "#6B7280", "gray.500"),
           "600": _scale("#4B5563", "#4B5563", "gray.600"),
           "700": _scale("#374151", "#374151", "gray.700"),
           "800": _scale("#1F2937", "#1F2937", "gray.800"),
           "850": _scale("#161B22", "#161B22", "gray.850"),
           "900": _scale("#111827", "#111827", "gray.900")}
    ))
    blue: PaletteFamily = field(default_factory=lambda: PaletteFamily.with_values(
        **{"50": _scale("#EFF6FF", "#EFF6FF", "blue.50"),
           "100": _scale("#DBEAFE", "#DBEAFE", "blue.100"),
           "200": _scale("#BFDBFE", "#BFDBFE", "blue.200"),
           "300": _scale("#93C5FD", "#93C5FD", "blue.300"),
           "400": _scale("#60A5FA", "#60A5FA", "blue.400"),
           "500": _scale("#3B82F6", "#3B82F6", "blue.500"),
           "600": _scale("#2563EB", "#2563EB", "blue.600"),
           "700": _scale("#1D4ED8", "#1D4ED8", "blue.700"),
           "800": _scale("#1E40AF", "#1E40AF", "blue.800"),
           "900": _scale("#1E3A5F", "#1E3A5F", "blue.900")}
    ))
    red: PaletteFamily = field(default_factory=lambda: PaletteFamily.with_values(
        **{"50": _scale("#FEF2F2", "#FEF2F2", "red.50"),
           "100": _scale("#FEE2E2", "#FEE2E2", "red.100"),
           "200": _scale("#FECACA", "#FECACA", "red.200"),
           "300": _scale("#FCA5A5", "#FCA5A5", "red.300"),
           "400": _scale("#F87171", "#F87171", "red.400"),
           "500": _scale("#EF4444", "#EF4444", "red.500"),
           "600": _scale("#DC2626", "#DC2626", "red.600"),
           "700": _scale("#B91C1C", "#B91C1C", "red.700"),
           "800": _scale("#991B1B", "#991B1B", "red.800"),
           "900": _scale("#7F1D1D", "#7F1D1D", "red.900")}
    ))
    green: PaletteFamily = field(default_factory=lambda: PaletteFamily.with_values(
        **{"50": _scale("#F0FDF4", "#F0FDF4", "green.50"),
           "100": _scale("#DCFCE7", "#DCFCE7", "green.100"),
           "200": _scale("#BBF7D0", "#BBF7D0", "green.200"),
           "300": _scale("#86EFAC", "#86EFAC", "green.300"),
           "400": _scale("#4ADE80", "#4ADE80", "green.400"),
           "500": _scale("#22C55E", "#22C55E", "green.500"),
           "600": _scale("#16A34A", "#16A34A", "green.600"),
           "700": _scale("#15803D", "#15803D", "green.700"),
           "800": _scale("#166534", "#166534", "green.800"),
           "900": _scale("#14532D", "#14532D", "green.900")}
    ))
    purple: PaletteFamily = field(default_factory=lambda: PaletteFamily.with_values(
        **{"50": _scale("#FAF5FF", "#FAF5FF", "purple.50"),
           "100": _scale("#F3E8FF", "#F3E8FF", "purple.100"),
           "200": _scale("#E9D5FF", "#E9D5FF", "purple.200"),
           "300": _scale("#D8B4FE", "#D8B4FE", "purple.300"),
           "400": _scale("#C084FC", "#C084FC", "purple.400"),
           "500": _scale("#A855F7", "#A855F7", "purple.500"),
           "600": _scale("#9333EA", "#9333EA", "purple.600"),
           "700": _scale("#7E22CE", "#7E22CE", "purple.700"),
           "800": _scale("#6B21A8", "#6B21A8", "purple.800"),
           "900": _scale("#4C1D95", "#4C1D95", "purple.900")}
    ))
    orange: PaletteFamily = field(default_factory=lambda: PaletteFamily.with_values(
        **{"50": _scale("#FFF7ED", "#FFF7ED", "orange.50"),
           "100": _scale("#FFEDD5", "#FFEDD5", "orange.100"),
           "200": _scale("#FED7AA", "#FED7AA", "orange.200"),
           "300": _scale("#FDBA74", "#FDBA74", "orange.300"),
           "400": _scale("#FB923C", "#FB923C", "orange.400"),
           "500": _scale("#F97316", "#F97316", "orange.500"),
           "600": _scale("#EA580C", "#EA580C", "orange.600"),
           "700": _scale("#C24100", "#C24100", "orange.700"),
           "800": _scale("#9A3412", "#9A3412", "orange.800"),
           "900": _scale("#7C2D12", "#7C2D12", "orange.900")}
    ))
    yellow: PaletteFamily = field(default_factory=lambda: PaletteFamily.with_values(
        **{"50": _scale("#FFFBEB", "#FFFBEB", "yellow.50"),
           "100": _scale("#FEF3C7", "#FEF3C7", "yellow.100"),
           "200": _scale("#FDE68A", "#FDE68A", "yellow.200"),
           "300": _scale("#FCD34D", "#FCD34D", "yellow.300"),
           "400": _scale("#FBBF24", "#FBBF24", "yellow.400"),
           "500": _scale("#F59E0B", "#F59E0B", "yellow.500"),
           "600": _scale("#D97706", "#D97706", "yellow.600"),
           "700": _scale("#B45309", "#B45309", "yellow.700"),
           "800": _scale("#854D0E", "#854D0E", "yellow.800"),
           "900": _scale("#713F12", "#713F12", "yellow.900")}
    ))

    white: PaletteToken = _scale("#FFFFFF", "#FFFFFF", "white")
    black: PaletteToken = _scale("#000000", "#000000", "black")
    transparent: PaletteToken = PaletteToken("transparent", QColor(0, 0, 0, 0), QColor(0, 0, 0, 0))

    black_3: PaletteToken = PaletteToken("black_3", QColor(0, 0, 0, 8), QColor(0, 0, 0, 8))
    black_4: PaletteToken = PaletteToken("black_4", QColor(0, 0, 0, 11), QColor(0, 0, 0, 11))
    black_5: PaletteToken = PaletteToken("black_5", QColor(0, 0, 0, 13), QColor(0, 0, 0, 13))
    black_6: PaletteToken = PaletteToken("black_6", QColor(0, 0, 0, 15), QColor(0, 0, 0, 15))
    black_8: PaletteToken = PaletteToken("black_8", QColor(0, 0, 0, 21), QColor(0, 0, 0, 21))
    black_10: PaletteToken = PaletteToken("black_10", QColor(0, 0, 0, 26), QColor(0, 0, 0, 26))
    black_20: PaletteToken = PaletteToken("black_20", QColor(0, 0, 0, 51), QColor(0, 0, 0, 51))
    black_50: PaletteToken = PaletteToken("black_50", QColor(0, 0, 0, 128), QColor(0, 0, 0, 128))
    black_60: PaletteToken = PaletteToken("black_60", QColor(0, 0, 0, 153), QColor(0, 0, 0, 153))
    white_3: PaletteToken = PaletteToken("white_3", QColor(255, 255, 255, 8), QColor(255, 255, 255, 8))
    white_4: PaletteToken = PaletteToken("white_4", QColor(255, 255, 255, 11), QColor(255, 255, 255, 11))
    white_5: PaletteToken = PaletteToken("white_5", QColor(255, 255, 255, 13), QColor(255, 255, 255, 13))
    white_6: PaletteToken = PaletteToken("white_6", QColor(255, 255, 255, 15), QColor(255, 255, 255, 15))
    white_8: PaletteToken = PaletteToken("white_8", QColor(255, 255, 255, 21), QColor(255, 255, 255, 21))
    white_10: PaletteToken = PaletteToken("white_10", QColor(255, 255, 255, 26), QColor(255, 255, 255, 26))
    white_20: PaletteToken = PaletteToken("white_20", QColor(255, 255, 255, 51), QColor(255, 255, 255, 51))

    # ── WinUI 3 / Fluent 2 token primitives ───────────────────
    # Source: controls/dev/CommonStyles/Common_themeresources_any.xaml

    # ControlFillColorDefault / Secondary / Tertiary / Disabled
    btn_bg: PaletteToken = PaletteToken("btn_bg", QColor(255, 255, 255, 179), QColor(255, 255, 255, 15))
    btn_bg_hover: PaletteToken = PaletteToken("btn_bg_hover", QColor(249, 249, 249, 128), QColor(255, 255, 255, 21))
    btn_bg_pressed: PaletteToken = PaletteToken("btn_bg_pressed", QColor(249, 249, 249, 77), QColor(255, 255, 255, 8))
    btn_bg_disabled: PaletteToken = PaletteToken("btn_bg_disabled", QColor(249, 249, 249, 77), QColor(255, 255, 255, 11))

    # ControlStrokeColorDefault / ControlStrokeColorSecondary (for ControlElevationBorderBrush gradient)
    btn_border: PaletteToken = PaletteToken("btn_border", QColor(0, 0, 0, 15), QColor(255, 255, 255, 18))
    btn_border_accent: PaletteToken = PaletteToken("btn_border_accent", QColor(0, 0, 0, 41), QColor(255, 255, 255, 24))

    # Text fills (TextFillColorPrimary / Secondary / Tertiary / Disabled)
    text_primary: PaletteToken = PaletteToken("text_primary", QColor(0, 0, 0, 228), QColor(255, 255, 255, 255))
    text_secondary: PaletteToken = PaletteToken("text_secondary", QColor(0, 0, 0, 158), QColor(255, 255, 255, 197))
    text_tertiary: PaletteToken = PaletteToken("text_tertiary", QColor(0, 0, 0, 114), QColor(255, 255, 255, 135))
    text_disabled: PaletteToken = PaletteToken("text_disabled", QColor(0, 0, 0, 92), QColor(255, 255, 255, 93))

    # Stroke colours
    stroke_default: PaletteToken = PaletteToken("stroke_default", QColor(0, 0, 0, 15), QColor(255, 255, 255, 18))
    stroke_secondary: PaletteToken = PaletteToken("stroke_secondary", QColor(0, 0, 0, 41), QColor(255, 255, 255, 24))
    stroke_card: PaletteToken = PaletteToken("stroke_card", QColor(0, 0, 0, 15), QColor(0, 0, 0, 25))
    stroke_flyout: PaletteToken = PaletteToken("stroke_flyout", QColor(0, 0, 0, 15), QColor(0, 0, 0, 51))
    stroke_divider: PaletteToken = PaletteToken("stroke_divider", QColor(0, 0, 0, 15), QColor(255, 255, 255, 21))
    stroke_strong_default: PaletteToken = PaletteToken("stroke_strong_default", QColor(0, 0, 0, 114), QColor(255, 255, 255, 139))
    stroke_strong_disabled: PaletteToken = PaletteToken("stroke_strong_disabled", QColor(0, 0, 0, 55), QColor(255, 255, 255, 40))

    # ControlFillColorInputActive
    input_active_bg: PaletteToken = PaletteToken("input_active_bg", QColor(255, 255, 255, 255), QColor(30, 30, 30, 179))

    # SubtleFill colors (interactivity — hover/pressed overlays)
    subtle_secondary: PaletteToken = PaletteToken("subtle_secondary", QColor(0, 0, 0, 9), QColor(255, 255, 255, 15))
    subtle_tertiary: PaletteToken = PaletteToken("subtle_tertiary", QColor(0, 0, 0, 6), QColor(255, 255, 255, 10))

    # Focus stroke colours (inner + outer ring)
    focus_outer: PaletteToken = PaletteToken("focus_outer", QColor(0, 0, 0, 228), QColor(255, 255, 255, 255))
    focus_inner: PaletteToken = PaletteToken("focus_inner", QColor(255, 255, 255, 179), QColor(0, 0, 0, 179))

    # SolidBackgroundFill
    solid_bg_base: PaletteToken = PaletteToken("solid_bg_base", QColor(243, 243, 243), QColor(32, 32, 32))
    solid_bg_secondary: PaletteToken = PaletteToken("solid_bg_secondary", QColor(238, 238, 238), QColor(28, 28, 28))
    solid_bg_tertiary: PaletteToken = PaletteToken("solid_bg_tertiary", QColor(249, 249, 249), QColor(40, 40, 40))
    solid_bg_quarternary: PaletteToken = PaletteToken("solid_bg_quarternary", QColor(255, 255, 255), QColor(44, 44, 44))

    # Switch track off (FluentUI QML: light rgba(253,253,253,1) / dark rgba(50,50,50,1))
    switch_track_off: PaletteToken = PaletteToken("switch_track_off", QColor(253, 253, 253), QColor(50, 50, 50))
    # Switch track off border (FluentUI QML: light rgba(141,141,141,1) / dark rgba(161,161,161,1))
    switch_track_off_border: PaletteToken = PaletteToken("switch_track_off_border", QColor(141, 141, 141), QColor(161, 161, 161))
    # Switch track hovered (FluentUI QML: light rgba(240,240,240,1) / dark rgba(62,62,62,1))
    switch_track_hovered: PaletteToken = PaletteToken("switch_track_hovered", QColor(240, 240, 240), QColor(62, 62, 62))
    # Switch track disabled (FluentUI QML: light rgba(233,233,233,1) / dark rgba(82,82,82,1))
    switch_track_disabled: PaletteToken = PaletteToken("switch_track_disabled", QColor(233, 233, 233), QColor(82, 82, 82))
    # Switch border disabled (FluentUI QML: light rgba(200,200,200,1) / dark rgba(50,50,50,1))
    switch_border_disabled: PaletteToken = PaletteToken("switch_border_disabled", QColor(200, 200, 200), QColor(50, 50, 50))
    # Switch thumb off (FluentUI QML: light rgba(93,93,93,1) / dark rgba(208,208,208,1))
    switch_thumb_off: PaletteToken = PaletteToken("switch_thumb_off", QColor(93, 93, 93), QColor(208, 208, 208))
    # Switch thumb disabled (FluentUI QML: light rgba(150,150,150,1) / dark rgba(50,50,50,1))
    switch_thumb_disabled: PaletteToken = PaletteToken("switch_thumb_disabled", QColor(150, 150, 150), QColor(50, 50, 50))
    # Switch thumb checked (FluentUI QML: light rgba(255,255,255,1) / dark rgba(0,0,0,1))
    switch_thumb_checked: PaletteToken = PaletteToken("switch_thumb_checked", QColor(255, 255, 255), QColor(0, 0, 0))

    # ── FluControlBackground shadow (high-perf stacked border shadow) ──
    shadow_light: PaletteToken = PaletteToken("shadow_light", QColor(153, 153, 153), QColor(0, 0, 0))

    # ── TextBox background states (FluTextBoxBackground) ──
    textbox_bg_normal: PaletteToken = PaletteToken("textbox_bg_normal", QColor(254, 254, 254), QColor(62, 62, 62))
    textbox_bg_hovered: PaletteToken = PaletteToken("textbox_bg_hovered", QColor(251, 251, 251), QColor(68, 68, 68))
    textbox_bg_focused: PaletteToken = PaletteToken("textbox_bg_focused", QColor(255, 255, 255), QColor(36, 36, 36))
    textbox_bg_disabled: PaletteToken = PaletteToken("textbox_bg_disabled", QColor(252, 252, 252), QColor(59, 59, 59))
    textbox_border_start: PaletteToken = PaletteToken("textbox_border_start", QColor(232, 232, 232), QColor(66, 66, 66))
    textbox_border_end: PaletteToken = PaletteToken("textbox_border_end", QColor(132, 132, 132), QColor(123, 123, 123))

    # ── TextBox text colors (FluTextBox) ──
    textbox_text: PaletteToken = PaletteToken("textbox_text", QColor(27, 27, 27), QColor(255, 255, 255))
    textbox_text_disabled: PaletteToken = PaletteToken("textbox_text_disabled", QColor(160, 160, 160), QColor(131, 131, 131))
    textbox_placeholder: PaletteToken = PaletteToken("textbox_placeholder", QColor(96, 96, 96), QColor(210, 210, 210))
    textbox_placeholder_focus: PaletteToken = PaletteToken("textbox_placeholder_focus", QColor(141, 141, 141), QColor(152, 152, 152))
    textbox_placeholder_disabled: PaletteToken = PaletteToken("textbox_placeholder_disabled", QColor(160, 160, 160), QColor(131, 131, 131))

    # ── Button colors (FluButton) ──
    button_bg: PaletteToken = PaletteToken("button_bg", QColor(254, 254, 254), QColor(62, 62, 62))
    button_bg_hover: PaletteToken = PaletteToken("button_bg_hover", QColor(246, 246, 246), QColor(68, 68, 68))
    button_bg_disabled: PaletteToken = PaletteToken("button_bg_disabled", QColor(251, 251, 251), QColor(59, 59, 59))
    button_divider: PaletteToken = PaletteToken("button_divider", QColor(233, 233, 233), QColor(80, 80, 80))
    button_text_pressed: PaletteToken = PaletteToken("button_text_pressed", QColor(96, 96, 96), QColor(162, 162, 162))
    button_text_disabled: PaletteToken = PaletteToken("button_text_disabled", QColor(160, 160, 160), QColor(131, 131, 131))

    # ── CheckBox colors (FluCheckBox) ──
    checkbox_bg: PaletteToken = PaletteToken("checkbox_bg", QColor(247, 247, 247), QColor(45, 45, 45))
    checkbox_bg_hover: PaletteToken = PaletteToken("checkbox_bg_hover", QColor(236, 236, 236), QColor(72, 72, 72))
    checkbox_bg_disabled: PaletteToken = PaletteToken("checkbox_bg_disabled", QColor(253, 253, 253), QColor(50, 50, 50))
    checkbox_border: PaletteToken = PaletteToken("checkbox_border", QColor(136, 136, 136), QColor(160, 160, 160))
    checkbox_border_hover: PaletteToken = PaletteToken("checkbox_border_hover", QColor(135, 135, 135), QColor(167, 167, 167))
    checkbox_border_pressed: PaletteToken = PaletteToken("checkbox_border_pressed", QColor(191, 191, 191), QColor(90, 90, 90))
    checkbox_border_disabled: PaletteToken = PaletteToken("checkbox_border_disabled", QColor(199, 199, 199), QColor(82, 82, 82))
    checkbox_checked_disabled: PaletteToken = PaletteToken("checkbox_checked_disabled", QColor(199, 199, 199), QColor(82, 82, 82))

    # ── RadioButton colors (FluRadioButton) ──
    radio_bg: PaletteToken = PaletteToken("radio_bg", QColor(255, 255, 255), QColor(50, 50, 50))
    radio_bg_hover: PaletteToken = PaletteToken("radio_bg_hover", QColor(222, 222, 222), QColor(43, 43, 43))
    radio_bg_disabled: PaletteToken = PaletteToken("radio_bg_disabled", QColor(222, 222, 222), QColor(43, 43, 43))
    radio_bg_checked_disabled: PaletteToken = PaletteToken("radio_bg_checked_disabled", QColor(159, 159, 159), QColor(159, 159, 159))
    radio_border: PaletteToken = PaletteToken("radio_border", QColor(141, 141, 141), QColor(161, 161, 161))
    radio_border_disabled: PaletteToken = PaletteToken("radio_border_disabled", QColor(198, 198, 198), QColor(82, 82, 82))

    # ── Menu colors (FluMenu) ──
    menu_bg: PaletteToken = PaletteToken("menu_bg", QColor(252, 252, 252), QColor(45, 45, 45))
    menu_border: PaletteToken = PaletteToken("menu_border", QColor(191, 191, 191), QColor(26, 26, 26))

    # ── ComboBox popup colors ──
    combobox_popup_bg: PaletteToken = PaletteToken("combobox_popup_bg", QColor(255, 255, 255), QColor(43, 43, 43))
    combobox_popup_border: PaletteToken = PaletteToken("combobox_popup_border", QColor(191, 191, 191), QColor(26, 26, 26))

    # ── Slider colors (FluSlider) ──
    slider_handle: PaletteToken = PaletteToken("slider_handle", QColor(255, 255, 255), QColor(69, 69, 69))
    slider_track: PaletteToken = PaletteToken("slider_track", QColor(138, 138, 138), QColor(162, 162, 162))

    # ── SpinBox colors (FluSpinBox) ──
    spinbox_bg: PaletteToken = PaletteToken("spinbox_bg", QColor(255, 255, 255), QColor(62, 62, 62))
    spinbox_bg_hover: PaletteToken = PaletteToken("spinbox_bg_hover", QColor(251, 251, 251), QColor(68, 68, 68))
    spinbox_bg_focused: PaletteToken = PaletteToken("spinbox_bg_focused", QColor(255, 255, 255), QColor(36, 36, 36))
    spinbox_bg_disabled: PaletteToken = PaletteToken("spinbox_bg_disabled", QColor(252, 252, 252), QColor(59, 59, 59))
    spinbox_button_bg: PaletteToken = PaletteToken("spinbox_button_bg", QColor(232, 232, 232), QColor(56, 56, 56))
    spinbox_button_hover: PaletteToken = PaletteToken("spinbox_button_hover", QColor(224, 224, 224), QColor(64, 64, 64))
    spinbox_button_pressed: PaletteToken = PaletteToken("spinbox_button_pressed", QColor(216, 216, 216), QColor(72, 72, 72))
    spinbox_border: PaletteToken = PaletteToken("spinbox_border", QColor(240, 240, 240), QColor(76, 76, 76))
    spinbox_border_disabled: PaletteToken = PaletteToken("spinbox_border_disabled", QColor(237, 237, 237), QColor(73, 73, 73))

    # ── InfoBar colors (FluInfoBar) ──
    infobar_success: PaletteToken = PaletteToken("infobar_success", QColor(223, 246, 221), QColor(57, 61, 27))
    infobar_warning: PaletteToken = PaletteToken("infobar_warning", QColor(255, 244, 206), QColor(67, 53, 25))
    infobar_info: PaletteToken = PaletteToken("infobar_info", QColor(244, 244, 244), QColor(39, 39, 39))
    infobar_error: PaletteToken = PaletteToken("infobar_error", QColor(253, 231, 233), QColor(68, 39, 38))

    # ── Badge colors ──
    badge_bg: PaletteToken = PaletteToken("badge_bg", QColor(255, 77, 79), QColor(255, 77, 79))

    # ── RatingControl colors ──
    rating_selected: PaletteToken = PaletteToken("rating_selected", QColor(0, 0, 0), QColor(255, 255, 255))

    def token(self, path: str) -> PaletteToken:
        parts = path.split(".")
        if len(parts) == 1:
            return getattr(self, parts[0])
        family = getattr(self, parts[0])
        return getattr(family, parts[1])

    def resolve(self, path: str, is_dark: bool) -> QColor:
        return self.token(path).for_mode(is_dark)
