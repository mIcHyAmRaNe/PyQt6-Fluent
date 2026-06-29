"""Palier 2 — Semantic roles. Maps a role name to a palette key per mode.

Organised into three families matching Fluent 2:
- neutral   → gray scale (structure, surfaces, text)
- shared    → red/green/orange/purple (status, feedback)
- brand     → blue (accent, link, selection)
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SemanticToken:
    name: str
    light_ref: str
    dark_ref: str

    def ref(self, is_dark: bool) -> str:
        return self.dark_ref if is_dark else self.light_ref


@dataclass
class SemanticPalette:
    # ── Neutral family: structure, surfaces, text ──────────────────
    surface: SemanticToken = field(default_factory=lambda: SemanticToken("surface", "gray.50", "gray.900"))

    # Surfaces
    surface_alt: SemanticToken = field(default_factory=lambda: SemanticToken("surface_alt", "gray.100", "gray.850"))
    surface_card: SemanticToken = field(default_factory=lambda: SemanticToken("surface_card", "white", "gray.800"))
    surface_dialog: SemanticToken = field(default_factory=lambda: SemanticToken("surface_dialog", "white", "gray.850"))

    # Text / icons on surface
    on_surface: SemanticToken = field(default_factory=lambda: SemanticToken("on_surface", "gray.900", "gray.50"))
    on_surface_muted: SemanticToken = field(default_factory=lambda: SemanticToken("on_surface_muted", "gray.500", "gray.400"))

    # Controls
    control_bg: SemanticToken = field(default_factory=lambda: SemanticToken("control_bg", "gray.100", "gray.800"))
    control_fg: SemanticToken = field(default_factory=lambda: SemanticToken("control_fg", "gray.900", "gray.50"))
    control_border: SemanticToken = field(default_factory=lambda: SemanticToken("control_border", "gray.200", "gray.700"))

    # Inputs
    input_bg: SemanticToken = field(default_factory=lambda: SemanticToken("input_bg", "white", "gray.800"))
    input_border: SemanticToken = field(default_factory=lambda: SemanticToken("input_border", "gray.300", "gray.600"))
    input_focus_border: SemanticToken = field(default_factory=lambda: SemanticToken("input_focus_border", "blue.500", "blue.400"))
    input_placeholder: SemanticToken = field(default_factory=lambda: SemanticToken("input_placeholder", "gray.400", "gray.500"))

    # Titlebar
    titlebar_bg: SemanticToken = field(default_factory=lambda: SemanticToken("titlebar_bg", "gray.100", "gray.800"))
    titlebar_fg: SemanticToken = field(default_factory=lambda: SemanticToken("titlebar_fg", "gray.900", "gray.50"))

    # Borders
    border: SemanticToken = field(default_factory=lambda: SemanticToken("border", "gray.200", "gray.700"))
    button_border: SemanticToken = field(default_factory=lambda: SemanticToken("button_border", "btn_border", "btn_border"))
    button_border_accent: SemanticToken = field(default_factory=lambda: SemanticToken("button_border_accent", "btn_border_accent", "btn_border_accent"))

    # Button backgrounds (Win11 solid colours)
    button_bg: SemanticToken = field(default_factory=lambda: SemanticToken("button_bg", "btn_bg", "btn_bg"))
    button_bg_hover: SemanticToken = field(default_factory=lambda: SemanticToken("button_bg_hover", "btn_bg_hover", "btn_bg_hover"))
    button_bg_pressed: SemanticToken = field(default_factory=lambda: SemanticToken("button_bg_pressed", "btn_bg_pressed", "btn_bg_pressed"))
    button_bg_disabled: SemanticToken = field(default_factory=lambda: SemanticToken("button_bg_disabled", "btn_bg_disabled", "btn_bg_disabled"))

    # Interactivity — Win11 precise fill values
    hover: SemanticToken = field(default_factory=lambda: SemanticToken("hover", "black_8", "white_8"))
    pressed: SemanticToken = field(default_factory=lambda: SemanticToken("pressed", "black_3", "white_3"))
    subtle_fill: SemanticToken = field(default_factory=lambda: SemanticToken("subtle_fill", "black_6", "white_6"))
    subtle_fill_disabled: SemanticToken = field(default_factory=lambda: SemanticToken("subtle_fill_disabled", "black_4", "white_4"))
    selected_bg: SemanticToken = field(default_factory=lambda: SemanticToken("selected_bg", "blue.100", "blue.800"))
    selected_fg: SemanticToken = field(default_factory=lambda: SemanticToken("selected_fg", "blue.900", "blue.50"))

    # Focus
    focus_ring: SemanticToken = field(default_factory=lambda: SemanticToken("focus_ring", "blue.500", "blue.400"))

    # Overlay
    overlay: SemanticToken = field(default_factory=lambda: SemanticToken("overlay", "black_50", "black_60"))

    # Links
    link: SemanticToken = field(default_factory=lambda: SemanticToken("link", "blue.600", "blue.400"))
    link_hover: SemanticToken = field(default_factory=lambda: SemanticToken("link_hover", "blue.700", "blue.300"))

    # Scrollbar
    scrollbar_bg: SemanticToken = field(default_factory=lambda: SemanticToken("scrollbar_bg", "gray.100", "gray.800"))
    scrollbar_fg: SemanticToken = field(default_factory=lambda: SemanticToken("scrollbar_fg", "gray.400", "gray.600"))

    # ── Shared family: status feedback ─────────────────────────────
    danger: SemanticToken = field(default_factory=lambda: SemanticToken("danger", "red.600", "red.300"))
    danger_bg: SemanticToken = field(default_factory=lambda: SemanticToken("danger_bg", "red.50", "red.900"))
    warning: SemanticToken = field(default_factory=lambda: SemanticToken("warning", "orange.600", "orange.300"))
    warning_bg: SemanticToken = field(default_factory=lambda: SemanticToken("warning_bg", "orange.50", "orange.900"))
    success: SemanticToken = field(default_factory=lambda: SemanticToken("success", "green.600", "green.300"))
    success_bg: SemanticToken = field(default_factory=lambda: SemanticToken("success_bg", "green.50", "green.900"))
    info: SemanticToken = field(default_factory=lambda: SemanticToken("info", "blue.600", "blue.300"))
    info_bg: SemanticToken = field(default_factory=lambda: SemanticToken("info_bg", "blue.50", "blue.900"))

    # ── Brand family: accent ───────────────────────────────────────
    accent: SemanticToken = field(default_factory=lambda: SemanticToken("accent", "blue.600", "blue.400"))
    accent_hover: SemanticToken = field(default_factory=lambda: SemanticToken("accent_hover", "blue.700", "blue.300"))
    accent_pressed: SemanticToken = field(default_factory=lambda: SemanticToken("accent_pressed", "blue.800", "blue.500"))
    on_accent: SemanticToken = field(default_factory=lambda: SemanticToken("on_accent", "white", "white"))

    # ── Close button (special — always red) ────────────────────────
    close_hover_bg: SemanticToken = field(default_factory=lambda: SemanticToken("close_hover_bg", "red.600", "red.600"))
    close_pressed_bg: SemanticToken = field(default_factory=lambda: SemanticToken("close_pressed_bg", "red.300", "red.300"))
    close_hover_fg: SemanticToken = field(default_factory=lambda: SemanticToken("close_hover_fg", "white", "white"))
    close_pressed_fg: SemanticToken = field(default_factory=lambda: SemanticToken("close_pressed_fg", "white", "white"))

    def token(self, name: str) -> SemanticToken:
        return getattr(self, name)

    def ref(self, name: str, is_dark: bool) -> str:
        return self.token(name).ref(is_dark)
