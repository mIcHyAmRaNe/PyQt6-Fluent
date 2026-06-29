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
    button_radius: int = 5

    input_height: int = 32
    input_padding_horizontal: int = 8
    input_padding_vertical: int = 4

    checkbox_size: int = 16
    radio_button_size: int = 16

    slider_height: int = 4
    slider_handle_size: int = 16
    slider_track: str = "palette.black_6"
    slider_fill: str = "semantic.accent"
    slider_thumb: str = "semantic.control_fg"

    scrollbar_width: int = 8
    scrollbar_handle_min_size: int = 24

    # Switch
    switch_width: int = 44
    switch_height: int = 20
    switch_thumb_size: int = 16
    switch_track_off: str = "palette.black_8"
    switch_track_on: str = "semantic.accent"
    switch_thumb: str = "palette.white"
    shadow: str = "semantic.shadow"
    shadow_blur: float = 16.0
    shadow_offset_y: float = 4.0

    # Scrollbar tokens (referenced from semantic)
    scrollbar_bg: str = "semantic.scrollbar_bg"
    scrollbar_fg: str = "semantic.scrollbar_fg"
