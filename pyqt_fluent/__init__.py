"""
PyQt6-Fluent — A Fluent Design component library for PyQt6.
"""

__version__ = "0.1.0"
__author__ = "Michy Amrane"

import sys

from PyQt6.QtWidgets import QDialog, QMainWindow

from .icons import FluentIcon, IconEngine, SvgIcon  # noqa: F401
from .icons.widget import IconWidget  # noqa: F401
from .presets import CATPPUCCIN_FRAPPE as catppuccinTheme  # noqa: F401
from .presets import DARK_THEME as darkTheme  # noqa: F401
from .presets import LIGHT_THEME as lightTheme  # noqa: F401
from .tokens.component import ComponentTokens  # noqa: F401
from .tokens.palette import Palette  # noqa: F401
from .tokens.resolver import TokenResolver  # noqa: F401
from .tokens.semantic import SemanticPalette  # noqa: F401
from .tokens.theme import ThemeDefinition, ThemeManager, ThemeMode, ThemeObserver  # noqa: F401
from .tokens.typography import Typography  # noqa: F401
from .utils import start_system_move, toggle_max_state  # noqa: F401
from .widgets._shared import (  # noqa: F401
    BackgroundAnimationWidget,
    DropShadow,
    FocusRing,
    RippleEffect,
    ThemeAwareWidget,
    TranslateYAnimation,
)
from .widgets.buttons import (  # noqa: F401
    # Legacy aliases
    AccentButton,
    Button,
    ButtonBase,
    FilledButton,
    HyperlinkButton,
    OutlinedButton,
    PushButton,
    Switch,
    TextButton,
    ToggleButton,
    TransparentButton,
)
from .widgets.data import DatePicker, NumberBox, TimePicker  # noqa: F401
from .widgets.feedback import Badge, ProgressBar, Spinner  # noqa: F401
from .widgets.inputs import Input, Rating, SearchBox, Slider, Tag, Textarea  # noqa: F401
from .widgets.layout import Card, Divider  # noqa: F401
from .widgets.misc import (  # noqa: F401
    Avatar,
    CommandBar,
    ContentDialog,
    Expander,
    FluentTooltip,
    InfoBar,
)
from .widgets.navigation import ComboBox, NavigationView, TabView  # noqa: F401
from .widgets.selection import CheckBox, RadioButton  # noqa: F401
from .widgets.text import FluentLabel  # noqa: F401
from .widgets.titlebar import StandardTitleBar, TitleBar, TitleBarBase  # noqa: F401
from .widgets.titlebar.title_bar_buttons import (  # noqa: F401
    CloseButton,
    MaximizeButton,
    MinimizeButton,
    SvgTitleBarButton,
    TitleBarButton,
)

if sys.platform == "win32":
    from .widgets.window.acrylic_window import AcrylicWindow
    from .widgets.window.frameless_window import FramelessWindow
    from .widgets.window.window_effect import WindowsWindowEffect as WindowEffect
elif sys.platform == "darwin":
    from .widgets.window.frameless_window import FramelessWindow
    from .widgets.window.window_effect import WindowsWindowEffect as WindowEffect
    AcrylicWindow = FramelessWindow
else:
    FramelessWindow = None
    AcrylicWindow = FramelessWindow
    WindowEffect = None


class FramelessDialog(QDialog, FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title_bar.min_btn.hide()
        self.title_bar.max_btn.hide()
        self.title_bar.set_double_click_enabled(False)
        self.window_effect.disable_maximize_button(self.winId())


class FramelessMainWindow(QMainWindow, FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent)


__all__ = [
    "__version__",
    "__author__",
    # Theme system
    "ThemeManager",
    "ThemeDefinition",
    "ThemeMode",
    "ThemeObserver",
    "Palette",
    "SemanticPalette",
    "ComponentTokens",
    "TokenResolver",
    "Typography",
    # Icon system
    "FluentIcon",
    "IconEngine",
    "IconWidget",
    "SvgIcon",
    # Window
    "FramelessWindow",
    "FramelessDialog",
    "FramelessMainWindow",
    "AcrylicWindow",
    "WindowEffect",
    # Shared primitives
    "ThemeAwareWidget",
    "BackgroundAnimationWidget",
    "TranslateYAnimation",
    # Titlebar
    "TitleBar",
    "TitleBarBase",
    "StandardTitleBar",
    "TitleBarButton",
    "SvgTitleBarButton",
    "MinimizeButton",
    "MaximizeButton",
    "CloseButton",
    # Buttons
    "Button",
    "ButtonBase",
    "PushButton",
    "AccentButton",
    "TransparentButton",
    "TextButton",
    "OutlinedButton",
    "HyperlinkButton",
    "FilledButton",
    "Switch",
    "ToggleButton",
    # Inputs
    "Input",
    "Rating",
    "SearchBox",
    "Slider",
    "Tag",
    "Textarea",
    # Selection
    "CheckBox",
    "RadioButton",
    # Feedback
    "Badge",
    "ProgressBar",
    "Spinner",
    # Layout
    "Card",
    "Divider",
    # Text
    "FluentLabel",
    # Navigation
    "ComboBox",
    "TabView",
    "NavigationView",
    # Data
    "DatePicker",
    "TimePicker",
    "NumberBox",
    # Misc
    "Avatar",
    "CommandBar",
    "ContentDialog",
    "Expander",
    "InfoBar",
    "FluentTooltip",
    # Utilities
    "start_system_move",
    "toggle_max_state",
    # Presets
    "lightTheme",
    "darkTheme",
    "catppuccinTheme",
]
