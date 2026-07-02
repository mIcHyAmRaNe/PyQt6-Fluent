import sys

from ..tokens.theme import ThemeMode  # noqa: F401
from .animation import winui_easing  # noqa: F401
from .color import blend, derive_accent_variants  # noqa: F401
from .dpi import DpiHelper  # noqa: F401
from .theme import Theme, is_dark, is_light, system_theme  # noqa: F401

if sys.platform == "win32":
    from .win32_utils import (
        ScreenCaptureFilter,
        get_system_accent_color,
    )
    from .win32_utils import (
        WindowsMoveResize as MoveResize,
    )
elif sys.platform == "darwin":
    try:
        from .mac_utils import MacMoveResize as MoveResize
        from .mac_utils import MacScreenCaptureFilter as ScreenCaptureFilter
        from .mac_utils import get_system_accent_color
    except ImportError:
        MoveResize = None
        ScreenCaptureFilter = None
        get_system_accent_color = None
else:
    try:
        from .linux_utils import LinuxMoveResize as MoveResize
        from .linux_utils import LinuxScreenCaptureFilter as ScreenCaptureFilter
        from .linux_utils import get_system_accent_color
    except ImportError:
        MoveResize = None
        ScreenCaptureFilter = None
        get_system_accent_color = None


def start_system_move(window, global_pos):
    MoveResize.start_system_move(window, global_pos)


def toggle_max_state(window):
    MoveResize.toggle_max_state(window)


def star_system_resize(window, global_pos, edges):
    MoveResize.star_system_resize(window, global_pos, edges)
