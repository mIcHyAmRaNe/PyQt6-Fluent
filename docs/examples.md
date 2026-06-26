# Examples Walkthrough

All examples are in `examples/`. Run them with:

```shell
uv run python -m examples.<name>
```

## demo.py — Minimal Frameless Window

**Shows:** `FramelessWindow` with `StandardTitleBar`, theme toggle button.

```python
from pyqt_fluent import FramelessWindow, StandardTitleBar, ThemeManager

class Window(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))
        self.setWindowTitle("PyQt-Frameless-Window")
        self.titleBar.raise_()

        self._themeBtn = QPushButton("Toggle Theme", self)
        self._themeBtn.clicked.connect(ThemeManager.instance().toggleTheme)
```

The `StandardTitleBar` shows window icon + title. The toggle button calls `ThemeManager.instance().toggleTheme()` which switches between light and dark, notifying all `ThemeObserver` instances.

## acrylic_demo.py — Acrylic Blur Window

**Shows:** `AcrylicWindow` with auto-adapting blur.

```python
from pyqt_fluent import AcrylicWindow

class Window(AcrylicWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acrylic Window")
        self.titleBar.raise_()
```

The acrylic gradient adapts to the system theme (dark → `1A1A1A99`, light → `F2F2F299`). Gradient is updated automatically via `_onSystemThemeChanged`.

To use a custom tint:

```python
self.windowEffect.setAcrylicEffect(self.winId(), "106EBE99")
```

## main_window.py — Full Text Editor

**Shows:** `FramelessMainWindow` with menus, `FramelessDialog` for dialogs.

```python
from pyqt_fluent import FramelessMainWindow, FramelessDialog

class MainWindow(FramelessMainWindow):
    def __init__(self):
        super().__init__()
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.setMenuWidget(self.titleBar)

        menuBar = QMenuBar(self.titleBar)
        self.titleBar.layout().insertWidget(0, menuBar, 0, Qt.AlignLeft)
```

### Dialogs

**ConfirmDialog** — Asks "Save changes?" with Save/Discard/Cancel buttons.

```python
class ConfirmDialog(FramelessDialog):
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        self.setResizeEnabled(False)
        # ... create UI, connect buttons
```

**AboutDialog** — Simple informational dialog.

```python
class AboutDialog(FramelessDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setResizeEnabled(False)
        # ... labels + OK button
        self.titleBar.raise_()
```

Both dialogs inherit from `FramelessDialog` → `QDialog, FramelessWindow`, so they get full frameless behaviour (drag, theme support, no system titlebar).

## theme_demo.py — Theme Switching Demo

**Shows:** Multiple theme presets and live switching.

Demonstrates `setLightTheme()`, `setDarkTheme()`, and applying the Catppuccin Frappé preset:

```python
from pyqt_fluent import catppuccinTheme
tm.setTheme(catppuccinTheme)
```

## catppuccin_demo.py — Catppuccin Frappé

**Shows:** Custom preset with Gabriola handwriting font.

The Catppuccin Frappé preset overrides palette, semantic, component, and typography tokens:

```python
catppuccin_theme = ThemeDefinition(
    name="Catppuccin Frappé",
    mode=ThemeMode.LIGHT,
    palette=...,
    semantic=...,
    component=...,
    typography=Typography(fontFamily="Gabriola"),
)
```

## custom_styling.py — Per-Window Overrides

**Shows:** Window-level colour overrides (legacy API).

## screen_capture_filter.py — Privacy Filter

**Shows:** `ScreenCaptureFilter` to prevent screen capture.

```python
from pyqt_fluent.utils import ScreenCaptureFilter

window.installEventFilter(ScreenCaptureFilter(window))
```

## web_engine.py — Frameless WebEngine

**Shows:** `FramelessWebEngineView` integration.
