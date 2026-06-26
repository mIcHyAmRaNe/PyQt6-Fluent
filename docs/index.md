# PyQt6-Fluent

Modern Windows frameless window library for PyQt6 with a 3‑tier design‑system token engine, Win11 acrylic/mica, and live dark/light theming.

## Quick Start

```python
import sys
from PyQt6.QtWidgets import QApplication
from pyqt_fluent import FramelessWindow

class Window(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hello Frameless")
        self.titleBar.raise_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())
```

Run: `uv run python examples/demo.py`

## Installation

```shell
pip install pyqt6-fluent
```

Or from source:

```shell
git clone https://github.com/michyamrane/PyQt6-Fluent.git
cd PyQt6-Fluent
uv pip install -e .
```

## Package Structure

| Module | Description |
|---|---|
| `pyqt_fluent` | Public API, `FramelessDialog`, `FramelessMainWindow` |
| `pyqt_fluent.tokens` | 3‑tier token system (Palette, Semantic, Component, Resolver, Theme) |
| `pyqt_fluent.presets` | Pre‑built theme definitions (light, dark, Catppuccin) |
| `pyqt_fluent.styles` | QSS stylesheet engine (`StylesheetEngine`) |
| `pyqt_fluent.widgets._shared` | Shared paint primitives (FocusRing, RippleEffect, DropShadow, IconWidget) |
| `pyqt_fluent.widgets.titlebar` | Title bar components |
| `pyqt_fluent.widgets.window` | Window implementations (frameless, acrylic, effects) |
| `pyqt_fluent.widgets.buttons` | Buttons, checkbox, radio, toggle |
| `pyqt_fluent.widgets.inputs` | Text inputs, combo, slider, spin |
| `pyqt_fluent.widgets.navigation` | Menu, tab, breadcrumb |
| `pyqt_fluent.widgets.feedback` | MessageBox, tooltip, info bar |
| `pyqt_fluent.widgets.data` | List, table, tree views |
| `pyqt_fluent.widgets.media` | Image, video, chart |
| `pyqt_fluent.widgets.layout` | Card, flow, scroll |
| `pyqt_fluent.widgets.misc` | Label, icon, chat |
| `pyqt_fluent.utils` | Win32 helpers, theme detection |
| `pyqt_fluent.webengine` | Frameless WebEngine view |

## Key Concepts

- **3‑tier tokens**: Palette (primitives) → Semantic (roles) → Component (mappings)
- **ThemeManager** singleton: controls the active theme, notifies observers
- **ThemeObserver**: widgets implement this to react to theme changes
- **TokenResolver**: resolves any path (e.g. `component.window_bg`) through all 3 tiers
