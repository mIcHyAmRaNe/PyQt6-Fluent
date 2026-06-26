from PyQt6.QtGui import QColor

from ..tokens.component import ComponentTokens
from ..tokens.palette import Palette, PaletteFamily, PaletteToken
from ..tokens.semantic import SemanticPalette, SemanticToken
from ..tokens.theme import ThemeDefinition, ThemeMode
from ..tokens.typography import Typography


def _ct(name: str, hex_: str) -> PaletteToken:
    return PaletteToken(name, QColor(hex_), QColor(hex_))


CATPPUCCIN_PALETTE = Palette(
    gray=PaletteFamily.with_values(
        **{"50": _ct("ct.rosewater", "#f2d5cf"),
           "100": _ct("ct.flamingo", "#eebebe"),
           "200": _ct("ct.pink", "#f4b8e4"),
           "300": _ct("ct.mauve", "#ca9ee6"),
           "400": _ct("ct.red", "#e78284"),
           "500": _ct("ct.maroon", "#ea999c"),
           "600": _ct("ct.peach", "#ef9f76"),
           "700": _ct("ct.yellow", "#e5c890"),
           "800": _ct("ct.green", "#a6d189"),
           "900": _ct("ct.teal", "#81c8be")}
    ),
    blue=PaletteFamily.with_values(
        **{"50": _ct("ct.sky", "#99d1db"),
           "100": _ct("ct.sapphire", "#85c1dc"),
           "200": _ct("ct.blue", "#8caaee"),
           "300": _ct("ct.lavender", "#babbf1"),
           "400": _ct("ct.blue.400", "#8caaee"),
           "500": _ct("ct.blue.500", "#8caaee"),
           "600": _ct("ct.blue.600", "#8caaee"),
           "700": _ct("ct.blue.700", "#85c1dc"),
           "800": _ct("ct.blue.800", "#85c1dc"),
           "900": _ct("ct.blue.900", "#85c1dc")}
    ),
    white=_ct("white", "#FFFFFF"),
    black=_ct("black", "#000000"),
    transparent=PaletteToken("transparent", QColor(0, 0, 0, 0), QColor(0, 0, 0, 0)),
    black_10=PaletteToken("black_10", QColor(255, 255, 255, 26), QColor(0, 0, 0, 26)),
    black_20=PaletteToken("black_20", QColor(255, 255, 255, 51), QColor(0, 0, 0, 51)),
    black_50=PaletteToken("black_50", QColor(255, 255, 255, 60), QColor(0, 0, 0, 128)),
    black_60=PaletteToken("black_60", QColor(255, 255, 255, 80), QColor(0, 0, 0, 153)),
    white_10=PaletteToken("white_10", QColor(255, 255, 255, 26), QColor(255, 255, 255, 26)),
    white_20=PaletteToken("white_20", QColor(255, 255, 255, 51), QColor(255, 255, 255, 51)),
)

CATPPUCCIN_SEMANTIC = SemanticPalette(
    accent=SemanticToken("accent", "blue.200", "blue.200"),
    accent_hover=SemanticToken("accent_hover", "blue.100", "blue.100"),
    surface=SemanticToken("surface", "gray.50", "gray.50"),
    surface_alt=SemanticToken("surface_alt", "gray.100", "gray.100"),
    surface_card=SemanticToken("surface_card", "blue.50", "blue.50"),
    surface_dialog=SemanticToken("surface_dialog", "gray.50", "gray.50"),
    on_surface=SemanticToken("on_surface", "gray.300", "gray.300"),
    on_surface_muted=SemanticToken("on_surface_muted", "gray.200", "gray.200"),
    titlebar_bg=SemanticToken("titlebar_bg", "gray.100", "gray.100"),
    titlebar_fg=SemanticToken("titlebar_fg", "gray.300", "gray.300"),
)

CATPPUCCIN_COMPONENT = ComponentTokens(
    window_radius=10,
    control_radius=6,
    titlebar_height=36,
)

CATPPUCCIN_TYPOGRAPHY = Typography(
    fontFamily="Gabriola",
    fallbackFamilies=["Segoe Script", "Comic Sans MS", "Segoe UI"],
)

CATPPUCCIN_FRAPPE = ThemeDefinition(
    name="Catppuccin Frappé",
    mode=ThemeMode.LIGHT,
    palette=CATPPUCCIN_PALETTE,
    semantic=CATPPUCCIN_SEMANTIC,
    component=CATPPUCCIN_COMPONENT,
    typography=CATPPUCCIN_TYPOGRAPHY,
)
