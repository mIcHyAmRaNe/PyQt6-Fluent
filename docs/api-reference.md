# API Reference

## Top-Level (`pyqt_fluent`)

### Window Classes

#### `FramelessWindow`

`FramelessWindow(QWidget, ThemeObserver)` — Base frameless window.

```python
from pyqt_fluent import FramelessWindow

w = FramelessWindow()
w.setWindowTitle("My Window")
w.titleBar.raise_()
```

**Properties:**
- `windowEffect: WindowsWindowEffect` — Win32 effect controller
- `titleBar: TitleBar` — Default titlebar (created in `__init__`)

**Methods:**
| Method | Description |
|---|---|
| `setTitleBar(titleBar)` | Replace the title bar with a custom one |
| `setResizeEnabled(bool)` | Enable/disable window resize |
| `setStayOnTop(bool)` | Toggle always-on-top |
| `updateFrameless()` | Re-apply frameless window styles |
| `setLightTheme()` / `setDarkTheme()` / `toggleTheme()` | Convenience wrappers for `ThemeManager` |

#### `FramelessMainWindow`

`FramelessMainWindow(QMainWindow, FramelessWindow)` — For `QMainWindow` layouts.

```python
from pyqt_fluent import FramelessMainWindow

mw = FramelessMainWindow()
mw.setCentralWidget(QTextEdit())
mw.setMenuWidget(mw.titleBar)
```

Supports all `QMainWindow` features: `setCentralWidget`, `setMenuWidget`, `setStatusBar`, `addToolBar`, etc.

#### `FramelessDialog`

`FramelessDialog(QDialog, FramelessWindow)` — Modal dialog without titlebar buttons.

```python
from pyqt_fluent import FramelessDialog

d = FramelessDialog()
d.setResizeEnabled(False)  # Fixed-size dialog
d.titleBar.raise_()
d.exec()
```

Minimize and maximize buttons are hidden. Double-click to toggle maximize is disabled.

#### `AcrylicWindow`

`AcrylicWindow(FramelessWindow)` — Window with Win10+ acrylic blur effect.

```python
from pyqt_fluent import AcrylicWindow

class MyAcrylicWindow(AcrylicWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acrylic")
```

The acrylic gradient auto-adapts to dark/light system theme. Update gradient manually:

```python
self.windowEffect.setAcrylicEffect(self.winId(), gradientColor="106EBE99")
```

### Theme API

#### `ThemeManager`

Singleton — use `ThemeManager.instance()`.

| Method | Description |
|---|---|
| `setTheme(theme: ThemeDefinition)` | Apply a theme, notify all observers |
| `setLightTheme()` | Apply the light preset |
| `setDarkTheme()` | Apply the dark preset |
| `toggleTheme()` | Switch between light and dark |
| `theme() -> ThemeDefinition` | Get the current theme |
| `resolve(path: str) -> Any` | Shorthand: `theme().resolve(path)` |
| `registerObserver(ThemeObserver)` | Start listening for theme changes |
| `unregisterObserver(ThemeObserver)` | Stop listening |
| `generateStylesheet() -> str` | Generate QSS for common widgets |

**Signals:**
| Signal | Description |
|---|---|
| `themeChanged(ThemeDefinition)` | Emitted when the theme changes |

#### `ThemeDefinition`

A dataclass combining all three tiers.

| Property | Type | Description |
|---|---|---|
| `name` | `str` | Theme human-readable name |
| `mode` | `ThemeMode` | `LIGHT` or `DARK` |
| `palette` | `Palette` | Primitive colour tokens |
| `semantic` | `SemanticPalette` | Semantic role tokens |
| `component` | `ComponentTokens` | Component mapping tokens |
| `typography` | `Typography` | Font definitions |

**Methods:**
| Method | Description |
|---|---|
| `isDark -> bool` | True if mode is DARK |
| `resolver() -> TokenResolver` | Get a resolver for this theme |
| `resolve(path: str) -> Any` | Shortcut: `resolver().resolve(path)` |
| `color(path: str) -> QColor` | Shortcut: `resolver().color(path)` |
| `copyWith(**overrides) -> ThemeDefinition` | Create a copy with overridden component values |

### Token System

#### `Palette`

Top-level palette holding all colour families.

```python
p = Palette()
p.gray._data["50"]          # PaletteToken for gray.50
p.blue._data["600"]         # PaletteToken for blue.600
p.white                     # PaletteToken
p.black_10                  # PaletteToken (alpha 10%)
```

#### `SemanticPalette`

Semantic roles with mode-dependent references, organised into three families.

```python
s = SemanticPalette()
s.titlebar_bg               # SemanticToken
s.surface                   # SemanticToken
s.input_placeholder         # input family
s.scrollbar_bg              # scrollbar family
```

**Neutral family:** `surface`, `surface_alt`, `surface_card`, `surface_dialog`, `on_surface`, `on_surface_muted`, `control_bg`, `control_fg`, `control_border`, `input_bg`, `input_border`, `input_focus_border`, `input_placeholder`, `titlebar_bg`, `titlebar_fg`, `border`, `hover`, `pressed`, `selected_bg`, `selected_fg`, `focus_ring`, `overlay`, `link`, `link_hover`, `scrollbar_bg`, `scrollbar_fg`

**Shared family:** `danger`, `danger_bg`, `warning`, `warning_bg`, `success`, `success_bg`, `info`, `info_bg`

**Brand family:** `accent`, `accent_hover`, `on_accent`, `close_hover_bg`, `close_pressed_bg`, `close_hover_fg`, `close_pressed_fg`

#### `ControlState`

Frozen dataclass holding 4 token string references for widget states.

```python
from pyqt_fluent.tokens import ControlState

btn = ControlState(rest="semantic.accent", hover="semantic.accent_hover",
                   pressed="semantic.accent", disabled="palette.transparent")
```

| Field | Default | Description |
|---|---|---|
| `rest` | `"palette.transparent"` | Default state colour ref |
| `hover` | `"semantic.hover"` | Hover state colour ref |
| `pressed` | `"semantic.pressed"` | Pressed state colour ref |
| `disabled` | `"palette.transparent"` | Disabled state colour ref |

#### `ComponentTokens`

Widget-level token mappings using `ControlState` for multi-state values.

```python
c = ComponentTokens()
c.window_bg                 # str -> "semantic.surface"
c.window_radius             # int -> 8
c.titlebar_button           # ControlState
c.titlebar_button.rest      # str
c.button_primary            # ControlState
c.button_primary.hover      # str
c.disabled_opacity          # float -> 0.4
```

**Input tokens:** `input_bg`, `input_fg`, `input_border`, `input_focus_border`, `input_placeholder`

**Widget metrics:** `window_radius`, `control_radius`, `overlay_radius`, `titlebar_height`, `titlebar_button_width`, `spacing`, `border_width`, `button_height`, `button_padding_horizontal`, `button_padding_vertical`, `input_height`, `input_padding_horizontal`, `input_padding_vertical`, `checkbox_size`, `radio_button_size`, `slider_height`, `slider_handle_size`, `scrollbar_width`, `scrollbar_handle_min_size`

#### `TokenResolver`

Chains all three layers. Supports dot-separated paths through `ControlState` fields.

```python
r = TokenResolver(palette, semantic, component, isDark)
r.resolve("component.window_bg")            # Any
r.color("component.window_bg")              # QColor
r.color("component.titlebar_button.hover")  # QColor — resolves through ControlState
r.int("component.window_radius")            # int
r.str("component.titlebar_height")          # str
```

### StylesheetEngine

Generates QSS by interpolating `{{token.path}}` expressions.

```python
from pyqt_fluent.styles import StylesheetEngine

engine = StylesheetEngine(resolver, typography)
qss = engine.generate("QPushButton")
engine.register("MyWidget", "background: {{component.window_bg}};")
```

**Methods:**
| Method | Description |
|---|---|
| `register(widget_type, rule)` | Register a custom QSS rule |
| `unregister(widget_type)` | Remove a registered rule |
| `generate(widget_type) -> str` | Return QSS for a widget type |
| `stylesheets(*widget_types) -> dict[str, str]` | Batch generate |

### Shared Widget Primitives

Reusable paint helpers under `pyqt_fluent.widgets._shared`.

#### `FocusRing`

Paint a Win11-style keyboard focus indicator.

```python
from pyqt_fluent import FocusRing

# In paintEvent:
FocusRing.paint(painter, self.rect(), QColor("#60a5fa"), radius=4, width=2)
```

#### `RippleEffect`

Material-style click ripple animation.

```python
from pyqt_fluent import RippleEffect

self._ripple = RippleEffect(self, color=QColor(255, 255, 255, 80))
# In mousePressEvent:
self._ripple.start(event.position())
# In paintEvent:
self._ripple.paint(painter, self.rect())
```

#### `DropShadow`

Anti-aliased drop shadow rendered directly in paintEvent.

```python
from pyqt_fluent import DropShadow

# In paintEvent:
DropShadow.paint(painter, self.rect(), color=QColor(0, 0, 0, 40),
                 radius=8, offset=(0, 2), spread=4)
```

#### `IconWidget`

Theme-aware SVG icon widget with colour replacement.

```python
from pyqt_fluent import IconWidget

icon = IconWidget(":/path/to/icon.svg")
icon.setColor(QColor("#ffffff"))
```

### Titlebar Classes

| Class | Description |
|---|---|
| `TitleBarBase(QWidget, ThemeObserver)` | Base: buttons, drag, double-click toggle |
| `TitleBar(TitleBarBase)` | Buttons right-aligned |
| `StandardTitleBar(TitleBar)` | + window icon + title label |

**TitleBarBase properties:**
- `minBtn: MinimizeButton`
- `maxBtn: MaximizeButton`
- `closeBtn: CloseButton`

**TitleBarBase methods:**
| Method | Description |
|---|---|
| `setDoubleClickEnabled(bool)` | Enable/disable double-click to maximize |

### Titlebar Buttons

| Class | Description |
|---|---|
| `TitleBarButton(QAbstractButton, ThemeObserver)` | Theme-aware base button |
| `SvgTitleBarButton(TitleBarButton)` | Button with SVG icon |
| `MinimizeButton(TitleBarButton)` | Minimize line icon |
| `MaximizeButton(TitleBarButton)` | Maximize rect icon (tracks state) |
| `CloseButton(SvgTitleBarButton)` | SVG close + red hover |

### Window Effects (`WindowsWindowEffect`)

| Method | Description |
|---|---|
| `setAcrylicEffect(hWnd, gradientColor, enableShadow, animationId)` | Win10+ acrylic |
| `setMicaEffect(hWnd, isDarkMode, isAlt)` | Win11 mica / mica alt |
| `setDarkMode(hWnd, isDark)` | DWM immersive dark mode |
| `setCaptionColor(hWnd, color)` | DWM caption area background |
| `setBorderAccentColor(hWnd, color)` | Win11 accent border |
| `removeBorderAccentColor(hWnd)` | Reset border to default |
| `addShadowEffect(hWnd)` | Add DWM window shadow |
| `removeShadowEffect(hWnd)` | Remove DWM shadow |
| `addWindowAnimation(hWnd)` | Enable maximize/minimize animation |
| `removeWindowAnimation(hWnd)` | Disable maximize/minimize animation |
| `enableBlurBehindWindow(hWnd)` | Enable blur behind window (DWM) |
| `disableBlurBehindWindow(hWnd)` | Disable blur |

### Utilities

| Function | Description |
|---|---|
| `startSystemMove(window, pos)` | Start a window move operation |
| `toggleMaxState(window)` | Toggle maximize/restore |

**Win32 utilities (`pyqt_fluent.utils.win32_utils`):**
| Function | Description |
|---|---|
| `systemTheme() -> Theme` | Read Windows theme (registry) |
| `isDark() -> bool` | True if Windows is in dark mode |
| `isLight() -> bool` | True if Windows is in light mode |
| `getSystemAccentColor() -> QColor` | Windows accent colour |
| `isSystemBorderAccentEnabled() -> bool` | Whether accent colour is applied to borders |
