"""Palier 3 — Component mappings. References semantic roles, never primitives."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ControlState:
    rest: str = "palette.transparent"
    hover: str = "semantic.hover"
    pressed: str = "semantic.pressed"
    disabled: str = "palette.transparent"

    @classmethod
    def from_colors(
        cls,
        rest="palette.transparent",
        hover="semantic.hover",
        pressed="semantic.pressed",
        disabled="palette.transparent",
    ):
        return cls(rest=rest, hover=hover, pressed=pressed, disabled=disabled)


@dataclass
class ComponentTokens:
    # Window
    window_bg: str = "semantic.surface"
    window_fg: str = "semantic.on_surface"

    # Titlebar
    titlebar_bg: str = "semantic.titlebar_bg"
    titlebar_fg: str = "semantic.titlebar_fg"
    titlebar_button: ControlState = field(
        default_factory=lambda: ControlState(
            rest="semantic.titlebar_fg",
            hover="semantic.titlebar_fg",
            pressed="semantic.on_surface",
        )
    )
    titlebar_button_bg: ControlState = field(
        default_factory=lambda: ControlState(
            rest="palette.transparent",
            hover="semantic.hover",
            pressed="semantic.pressed",
        )
    )
    close_button_fg: ControlState = field(
        default_factory=lambda: ControlState(
            rest="semantic.titlebar_fg",
            hover="semantic.close_hover_fg",
            pressed="semantic.close_pressed_fg",
        )
    )
    close_button_bg: ControlState = field(
        default_factory=lambda: ControlState(
            rest="palette.transparent",
            hover="semantic.close_hover_bg",
            pressed="semantic.close_pressed_bg",
        )
    )

    # Content
    content_bg: str = "semantic.surface_card"
    content_fg: str = "semantic.on_surface"
    card_bg: str = "semantic.surface_card"
    border: str = "semantic.border"

    # Inputs
    input_bg: str = "semantic.input_bg"
    input_fg: str = "semantic.on_surface"
    input_border: str = "semantic.input_border"
    input_focus_border: str = "semantic.input_focus_border"
    input_placeholder: str = "semantic.input_placeholder"

    # ── Button family ────────────────────────────────────────────
    button_standard: ControlState = field(
        default_factory=lambda: ControlState(
            rest="semantic.button_bg",
            hover="semantic.button_bg_hover",
            pressed="semantic.button_bg_pressed",
            disabled="semantic.button_bg_disabled",
        )
    )
    button_standard_fg: str = "semantic.control_fg"
    button_standard_border: str = "semantic.button_border"
    button_standard_border_accent: str = "semantic.button_border_accent"

    button_accent: ControlState = field(
        default_factory=lambda: ControlState(
            rest="semantic.accent",
            hover="semantic.accent_hover",
            pressed="semantic.accent_pressed",
            disabled="semantic.accent",
        )
    )
    button_accent_fg: str = "semantic.on_accent"
    button_accent_border: str = "palette.transparent"

    button_transparent: ControlState = field(
        default_factory=lambda: ControlState(
            rest="palette.transparent",
            hover="semantic.hover",
            pressed="semantic.pressed",
            disabled="palette.transparent",
        )
    )
    button_transparent_fg: str = "semantic.control_fg"
    button_transparent_border: str = "palette.transparent"

    button_text: ControlState = field(
        default_factory=lambda: ControlState(
            rest="palette.transparent",
            hover="semantic.hover",
            pressed="semantic.pressed",
            disabled="palette.transparent",
        )
    )
    button_text_fg: str = "semantic.accent"
    button_text_border: str = "palette.transparent"

    button_outlined: ControlState = field(
        default_factory=lambda: ControlState(
            rest="palette.transparent",
            hover="semantic.hover",
            pressed="semantic.pressed",
            disabled="palette.transparent",
        )
    )
    button_outlined_fg: str = "semantic.control_fg"
    button_outlined_border: str = "semantic.button_border"

    button_hyperlink: ControlState = field(
        default_factory=lambda: ControlState(
            rest="palette.transparent",
            hover="semantic.hover",
            pressed="semantic.pressed",
            disabled="palette.transparent",
        )
    )
    button_hyperlink_fg: str = "semantic.link"
    button_hyperlink_border: str = "palette.transparent"

    button_filled: ControlState = field(
        default_factory=lambda: ControlState(
            rest="semantic.control_bg",
            hover="semantic.hover",
            pressed="semantic.pressed",
            disabled="semantic.control_bg",
        )
    )
    button_filled_fg: str = "semantic.control_fg"
    button_filled_border: str = "palette.transparent"

    # Dialog
    dialog_bg: str = "semantic.surface_dialog"
    dialog_overlay: str = "semantic.overlay"

    # Acrylic
    acrylic_gradient: str = "palette.white"

    # Disabled
    disabled_opacity: float = 0.4

    # Geometry
    window_radius: int = 8
    control_radius: int = 4
    overlay_radius: int = 8
    titlebar_height: int = 32
    titlebar_button_width: int = 46
    spacing: int = 4
    border_width: int = 1

    # Widget-specific metrics
    button_height: int = 32
    button_padding_horizontal: int = 12
    button_padding_vertical: int = 4
    button_radius: int = 4

    input_height: int = 32
    input_padding_horizontal: int = 8
    input_padding_vertical: int = 4

    checkbox_size: int = 18
    radio_button_size: int = 18

    slider_height: int = 6
    slider_handle_size: int = 20
    slider_track: str = "palette.black_6"
    slider_fill: str = "semantic.accent"
    slider_thumb: str = "semantic.control_fg"

    scrollbar_width: int = 8
    scrollbar_handle_min_size: int = 24

    # ── ProgressBar ────────────────────────────────────────
    progressbar_height: int = 6
    progressbar_radius: int = 3
    progressbar_rail: str = "palette.stroke_default"
    progressbar_fill: str = "semantic.accent"

    # Switch
    switch_width: int = 40
    switch_height: int = 20
    switch_thumb_size: int = 16
    switch_track_off: str = "palette.switch_track_off"
    switch_track_on: str = "semantic.accent"
    switch_thumb: str = "semantic.switch_thumb"
    shadow: str = "palette.black_20"
    shadow_blur: float = 16.0
    shadow_offset_y: float = 4.0

    # ── Animation durations (WinUI 3 / Fluent 2) ─────────────
    # From Microsoft docs: cubic-bezier(0,0,0,1) durations
    duration_fast: int = 83       # Fade in/out
    duration_normal: int = 167    # Direct entrance/exit, micro-interactions
    duration_medium: int = 250    # Existing elements point-to-point
    duration_slow: int = 333      # Strong entrance
    progress_indeterminate_duration: int = 888  # FluUI standard

    # Scrollbar tokens (referenced from semantic)
    scrollbar_bg: str = "semantic.scrollbar_bg"
    scrollbar_fg: str = "semantic.scrollbar_fg"

    # ── ComboBox ──────────────────────────────────────────
    combobox_bg: str = "semantic.input_bg"
    combobox_fg: str = "semantic.on_surface"
    combobox_border: str = "semantic.input_border"
    combobox_focus_border: str = "semantic.input_focus_border"
    combobox_dropdown_bg: str = "semantic.surface_dialog"
    combobox_item_hover: str = "semantic.hover"
    combobox_item_selected: str = "semantic.selected_bg"
    combobox_item_selected_fg: str = "semantic.selected_fg"
    combobox_arrow: str = "semantic.control_fg"

    # ── DatePicker / TimePicker ───────────────────────────
    picker_bg: str = "semantic.input_bg"
    picker_fg: str = "semantic.on_surface"
    picker_border: str = "semantic.input_border"
    picker_focus_border: str = "semantic.input_focus_border"
    picker_popup_bg: str = "semantic.surface_dialog"
    picker_header_bg: str = "semantic.accent"
    picker_header_fg: str = "semantic.on_accent"
    picker_day_hover: str = "semantic.hover"
    picker_day_selected_bg: str = "semantic.accent"
    picker_day_selected_fg: str = "semantic.on_accent"
    picker_day_today_border: str = "semantic.accent"

    # ── NumberBox ─────────────────────────────────────────
    numberbox_bg: str = "semantic.input_bg"
    numberbox_fg: str = "semantic.on_surface"
    numberbox_border: str = "semantic.input_border"
    numberbox_focus_border: str = "semantic.input_focus_border"
    numberbox_button_bg: str = "semantic.button_bg"
    numberbox_button_hover: str = "semantic.button_bg_hover"
    numberbox_button_pressed: str = "semantic.button_bg_pressed"

    # ── TabView ───────────────────────────────────────────
    tab_bg: str = "palette.transparent"
    tab_selected_bg: str = "semantic.surface_card"
    tab_hover_bg: str = "semantic.hover"
    tab_fg: str = "semantic.on_surface"
    tab_selected_fg: str = "semantic.on_surface"
    tab_border: str = "semantic.border"
    tab_bar_bg: str = "palette.transparent"
    tab_close_hover: str = "semantic.hover"

    # ── Expander ──────────────────────────────────────────
    expander_header_bg: str = "palette.transparent"
    expander_header_hover: str = "semantic.hover"
    expander_content_bg: str = "palette.transparent"
    expander_arrow: str = "semantic.control_fg"
    expander_border: str = "semantic.border"

    # ── InfoBar / Toast ───────────────────────────────────
    infobar_border: str = "semantic.border"
    infobar_info_bg: str = "semantic.info_bg"
    infobar_info_fg: str = "semantic.on_surface"
    infobar_success_bg: str = "semantic.success_bg"
    infobar_success_fg: str = "semantic.on_surface"
    infobar_warning_bg: str = "semantic.warning_bg"
    infobar_warning_fg: str = "semantic.on_surface"
    infobar_danger_bg: str = "semantic.danger_bg"
    infobar_danger_fg: str = "semantic.on_surface"

    # ── Tooltip ───────────────────────────────────────────
    tooltip_bg: str = "semantic.surface_dialog"
    tooltip_fg: str = "semantic.on_surface"

    # ── Avatar / PersonPicture ────────────────────────────
    avatar_bg: str = "semantic.accent"
    avatar_fg: str = "semantic.on_accent"

    # ── CommandBar ────────────────────────────────────────
    commandbar_bg: str = "semantic.surface_card"
    commandbar_fg: str = "semantic.control_fg"
    commandbar_item_hover: str = "semantic.hover"
    commandbar_item_pressed: str = "semantic.pressed"
    commandbar_border: str = "semantic.border"
    commandbar_separator: str = "semantic.border"

    # ── NavigationView ────────────────────────────────────
    nav_bg: str = "semantic.surface_alt"
    nav_fg: str = "semantic.on_surface"
    nav_item_hover: str = "semantic.hover"
    nav_item_pressed: str = "semantic.pressed"
    nav_selected_bg: str = "semantic.selected_bg"
    nav_selected_fg: str = "semantic.selected_fg"
    nav_pill_accent: str = "semantic.nav_pill_accent"
    nav_border: str = "semantic.border"
    nav_width: int = 240
    nav_collapsed_width: int = 48
    nav_header_height: int = 48
    nav_item_height: int = 36

    # ── ContentDialog ─────────────────────────────────────
    contentdialog_bg: str = "semantic.surface_dialog"
    contentdialog_overlay: str = "semantic.overlay"
    contentdialog_radius: int = 8
