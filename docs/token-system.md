# 3‑Tier Token System

The entire design system is built on three indirection layers. No widget ever reads a primitive colour directly.

## Layer 1: Palette (`tokens/palette.py`)

Raw colour primitives. Each shade has both light and dark values.

### Grey scale

| Token | Light | Dark |
|---|---|---|
| `gray.50` | `#F9FAFB` | `#F9FAFB` |
| `gray.100` | `#F3F4F6` | `#F3F4F6` |
| `gray.200` | `#E5E7EB` | `#E5E7EB` |
| `gray.300` | `#D1D5DB` | `#D1D5DB` |
| `gray.400` | `#9CA3AF` | `#9CA3AF` |
| `gray.500` | `#6B7280` | `#6B7280` |
| `gray.600` | `#4B5563` | `#4B5563` |
| `gray.700` | `#374151` | `#374151` |
| `gray.800` | `#1F2937` | `#1F2937` |
| `gray.850` | `#161B22` | `#161B22` |
| `gray.900` | `#111827` | `#111827` |

### Colour families

`blue`, `red`, `green`, `purple`, `orange`, `yellow` — each has 50→900 shades with identical light/dark values.

### Atomic tokens

`white`, `black`, `transparent`, `black_10/20/50/60`, `white_10/20`.

## Layer 2: SemanticPalette (`tokens/semantic.py`)

Semantic roles organised into three families matching Fluent 2.

### Neutral family — structure, surfaces, text

| Token | Light ref | Dark ref | Purpose |
|---|---|---|---|
| `surface` | `gray.50` | `gray.900` | Window background |
| `surface_alt` | `gray.100` | `gray.800` | Alternative surface |
| `surface_card` | `white` | `gray.800` | Card background |
| `surface_dialog` | `white` | `gray.850` | Dialog background |
| `on_surface` | `gray.900` | `gray.50` | Primary text |
| `on_surface_muted` | `gray.500` | `gray.400` | Secondary text |
| `control_bg` | `gray.100` | `gray.800` | Control background |
| `control_fg` | `gray.900` | `gray.50` | Control text |
| `control_border` | `gray.200` | `gray.700` | Control border |
| `input_bg` | `white` | `gray.800` | Input field background |
| `input_border` | `gray.300` | `gray.600` | Input border |
| `input_focus_border` | `blue.500` | `blue.400` | Input focus border |
| `input_placeholder` | `gray.400` | `gray.500` | Placeholder text |
| `titlebar_bg` | `gray.100` | `gray.800` | Titlebar background |
| `titlebar_fg` | `gray.900` | `gray.50` | Titlebar text/icon colour |
| `border` | `gray.200` | `gray.700` | Borders |
| `hover` | `black_10` | `white_10` | Hover overlay |
| `pressed` | `black_20` | `white_20` | Pressed overlay |
| `selected_bg` | `blue.100` | `blue.800` | Selection background |
| `selected_fg` | `blue.900` | `blue.50` | Selection text |
| `focus_ring` | `blue.500` | `blue.400` | Keyboard focus ring |
| `overlay` | `black_50` | `black_60` | Modal overlay |
| `link` | `blue.600` | `blue.400` | Hyperlink |
| `link_hover` | `blue.700` | `blue.300` | Link hover |
| `scrollbar_bg` | `gray.100` | `gray.800` | Scrollbar track |
| `scrollbar_fg` | `gray.400` | `gray.600` | Scrollbar thumb |

### Shared family — status feedback

| Token | Light ref | Dark ref | Purpose |
|---|---|---|---|
| `danger` | `red.600` | `red.300` | Error text |
| `danger_bg` | `red.50` | `red.900` | Error background |
| `warning` | `orange.600` | `orange.300` | Warning text |
| `warning_bg` | `orange.50` | `orange.900` | Warning background |
| `success` | `green.600` | `green.300` | Success text |
| `success_bg` | `green.50` | `green.900` | Success background |
| `info` | `blue.600` | `blue.300` | Info text |
| `info_bg` | `blue.50` | `blue.900` | Info background |

### Brand family — accent / close button

| Token | Light ref | Dark ref | Purpose |
|---|---|---|---|
| `accent` | `blue.600` | `blue.400` | Accent/highlight |
| `accent_hover` | `blue.700` | `blue.300` | Accent hover |
| `on_accent` | `white` | `white` | Text on accent |
| `close_hover_bg` | `red.600` | `red.600` | Close button hover |
| `close_pressed_bg` | `red.300` | `red.300` | Close button pressed |

## Layer 3: ComponentTokens (`tokens/component.py`)

Widget-specific token mappings. These point to semantic or palette paths.

| Token | Resolves to | Type |
|---|---|---|
| `window_bg` | `semantic.surface` | QColor |
| `window_fg` | `semantic.on_surface` | QColor |
| `titlebar_bg` | `semantic.titlebar_bg` | QColor |
| `titlebar_fg` | `semantic.titlebar_fg` | QColor |
| `titlebar_button_normal_fg` | `semantic.titlebar_fg` | QColor |
| `titlebar_button_hover_fg` | `semantic.titlebar_fg` | QColor |
| `titlebar_button_pressed_fg` | `semantic.titlebar_fg` | QColor |
| `titlebar_button_normal_bg` | `transparent` | QColor |
| `titlebar_button_hover_bg` | `semantic.hover` | QColor |
| `titlebar_button_pressed_bg` | `semantic.pressed` | QColor |
| `close_hover_bg` | `semantic.close_hover_bg` | QColor |
| `close_pressed_bg` | `semantic.close_pressed_bg` | QColor |
| `close_hover_fg` | `semantic.close_hover_fg` | QColor |
| `close_pressed_fg` | `semantic.close_pressed_fg` | QColor |
| `window_radius` | — | int (8) |
| `titlebar_height` | — | int (32) |

## Resolver (`tokens/resolver.py`)

Chains all three layers. Supports four path formats:

```python
# Component token → semantic → palette → QColor
r.color("component.window_bg")

# Semantic token → palette → QColor
r.color("semantic.titlebar_fg")

# Direct palette access
r.color("gray.50")

# Integer token
r.int("component.window_radius")

# Raw value (string, int, QColor)
r.resolve("component.titlebar_height")
```

## ThemeManager (`tokens/theme.py`)

Singleton that holds the active `ThemeDefinition` and broadcasts changes.

```python
from pyqt_fluent import ThemeManager

tm = ThemeManager.instance()
tm.setLightTheme()
tm.setDarkTheme()
tm.toggleTheme()

# Get current theme
theme = tm.theme()
color = theme.color("component.window_bg")
```

### ThemeObserver

Widgets implement `ThemeObserver` to receive theme changes:

```python
from pyqt_fluent import ThemeObserver, ThemeManager, ThemeDefinition

class MyWidget(QWidget, ThemeObserver):
    def __init__(self):
        super().__init__()
        tm = ThemeManager.instance()
        tm.registerObserver(self)
        self._applyTheme(tm.theme())

    def onThemeChanged(self, theme: ThemeDefinition):
        self._applyTheme(theme)

    def _applyTheme(self, theme):
        bg = theme.color("component.window_bg")
        self.setStyleSheet(f"background: {bg.name()};")
```

### Presets

```python
from pyqt_fluent import lightTheme, darkTheme, catppuccinTheme

tm.setTheme(lightTheme)         # Light theme
tm.setTheme(darkTheme)          # Dark theme
tm.setTheme(catppuccinTheme)    # Catppuccin Frappé
```
