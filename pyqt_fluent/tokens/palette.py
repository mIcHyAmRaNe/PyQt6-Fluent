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
    def with_values(cls, **kw: PaletteToken) -> "PaletteFamily":
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

    # WinUI 3 / Fluent 2 button colours (Common_themeresources_any.xaml)
    # ControlFillColorDefault / Secondary / Tertiary / Disabled
    btn_bg: PaletteToken = PaletteToken("btn_bg", QColor(255, 255, 255, 179), QColor(255, 255, 255, 15))
    btn_bg_hover: PaletteToken = PaletteToken("btn_bg_hover", QColor(249, 249, 249, 128), QColor(255, 255, 255, 21))
    btn_bg_pressed: PaletteToken = PaletteToken("btn_bg_pressed", QColor(249, 249, 249, 77), QColor(255, 255, 255, 8))
    btn_bg_disabled: PaletteToken = PaletteToken("btn_bg_disabled", QColor(249, 249, 249, 77), QColor(255, 255, 255, 11))
    # ControlStrokeColorDefault + ControlStrokeColorSecondary (for ControlElevationBorderBrush gradient)
    btn_border: PaletteToken = PaletteToken("btn_border", QColor(0, 0, 0, 15), QColor(255, 255, 255, 18))
    btn_border_accent: PaletteToken = PaletteToken("btn_border_accent", QColor(0, 0, 0, 41), QColor(255, 255, 255, 24))

    def token(self, path: str) -> PaletteToken:
        parts = path.split(".")
        if len(parts) == 1:
            return getattr(self, parts[0])
        family = getattr(self, parts[0])
        return getattr(family, parts[1])

    def resolve(self, path: str, is_dark: bool) -> QColor:
        return self.token(path).for_mode(is_dark)
