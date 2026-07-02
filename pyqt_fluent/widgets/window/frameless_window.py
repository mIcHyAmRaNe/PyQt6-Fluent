from ctypes import cast, create_unicode_buffer
from ctypes.wintypes import LPRECT, MSG

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget
from win32more.Windows.Win32.Foundation import POINT as _POINT
from win32more.Windows.Win32.Foundation import RECT as _RECT
from win32more.Windows.Win32.Graphics import Gdi as _gdi
from win32more.Windows.Win32.System import DataExchange as _de
from win32more.Windows.Win32.UI import WindowsAndMessaging as _wm

from ...tokens.theme import ThemeDefinition, ThemeManager, ThemeObserver
from ...utils import win32_utils as win_utils
from ...utils.theme import ThemeMode, system_theme
from ...utils.win32_utils import Taskbar, get_system_accent_color, is_system_border_accent_enabled
from ..titlebar import TitleBar
from .c_structures import LPNCCALCSIZE_PARAMS
from .window_effect import WindowsWindowEffect

WM_SETTINGCHANGE = 0x001A


class FramelessWindow(QWidget, ThemeObserver):
    BORDER_WIDTH = 5

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.window_effect = WindowsWindowEffect(self)
        self.title_bar = TitleBar(self)
        self._is_resize_enabled = True
        self._tm = ThemeManager.instance()

        self.update_frameless()
        self._apply_theme(self._tm.theme())
        self._on_system_theme_changed()

        self.windowHandle().screenChanged.connect(self._on_screen_changed)
        self._tm.register_observer(self)

        self.resize(500, 500)
        self.title_bar.raise_()

    def on_theme_changed(self, theme: ThemeDefinition) -> None:
        self._apply_theme(theme)

    def _apply_theme(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        bg = r.color("component.window_bg")
        fg = r.color("component.window_fg")
        self.setStyleSheet(
            f"FramelessWindow {{ background-color: {bg.name()}; color: {fg.name()}; }}"
        )

    def update_frameless(self):
        stay_on_top = (
            Qt.WindowType.WindowStaysOnTopHint
            if self.windowFlags() & Qt.WindowType.WindowStaysOnTopHint
            else 0
        )
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint | stay_on_top)
        self.window_effect.add_window_animation(self.winId())
        if type(self).__name__ != "AcrylicWindow":
            self.window_effect.add_shadow_effect(self.winId())

    def set_title_bar(self, title_bar):
        self.title_bar.deleteLater()
        self.title_bar.hide()
        self.title_bar = title_bar
        self.title_bar.setParent(self)
        self.title_bar.raise_()

    def set_resize_enabled(self, is_enabled: bool):
        self._is_resize_enabled = is_enabled

    def set_stay_on_top(self, is_top: bool):
        if is_top:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        self.update_frameless()
        self.show()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.title_bar.resize(self.width(), self.title_bar.height())

    def nativeEvent(self, event_type, message):
        msg = MSG.from_address(message.__int__())
        if not msg.hWnd:
            return super().nativeEvent(event_type, message)

        if msg.message == _wm.WM_NCHITTEST and self._is_resize_enabled:
            return self._handle_nc_hit_test(msg)
        elif msg.message == _wm.WM_NCCALCSIZE:
            return self._handle_nc_calc_size(msg)
        elif msg.message == WM_SETTINGCHANGE:
            return self._handle_setting_change(msg)
        elif msg.message == _wm.WM_SETFOCUS and is_system_border_accent_enabled():
            self.window_effect.set_border_accent_color(self.winId(), get_system_accent_color())
        elif msg.message == _wm.WM_KILLFOCUS and is_system_border_accent_enabled():
            self.window_effect.remove_border_accent_color(self.winId())

        return False, 0

    def _handle_nc_hit_test(self, msg):
        pt = _POINT()
        _wm.GetCursorPos(pt)
        _gdi.ScreenToClient(msg.hWnd, pt)
        x_pos, y_pos = pt.x, pt.y
        rc = _RECT()
        _wm.GetClientRect(msg.hWnd, rc)
        w = rc.right - rc.left
        h = rc.bottom - rc.top
        bw = (
            0
            if win_utils.is_maximized(msg.hWnd) or win_utils.is_full_screen(msg.hWnd)
            else self.BORDER_WIDTH
        )
        lx = x_pos < bw
        rx = x_pos > w - bw
        ty = y_pos < bw
        by = y_pos > h - bw
        if lx and ty:
            return True, _wm.HTTOPLEFT
        elif rx and by:
            return True, _wm.HTBOTTOMRIGHT
        elif rx and ty:
            return True, _wm.HTTOPRIGHT
        elif lx and by:
            return True, _wm.HTBOTTOMLEFT
        elif ty:
            return True, _wm.HTTOP
        elif by:
            return True, _wm.HTBOTTOM
        elif lx:
            return True, _wm.HTLEFT
        elif rx:
            return True, _wm.HTRIGHT
        return False, 0

    def _handle_nc_calc_size(self, msg):
        if msg.wParam:
            rect = cast(msg.lParam, LPNCCALCSIZE_PARAMS).contents.rgrc[0]
        else:
            rect = cast(msg.lParam, LPRECT).contents
        is_max = win_utils.is_maximized(msg.hWnd)
        is_full = win_utils.is_full_screen(msg.hWnd)
        if is_max and not is_full:
            ty = win_utils.get_resize_border_thickness(msg.hWnd, False)
            rect.top += ty
            rect.bottom -= ty
            tx = win_utils.get_resize_border_thickness(msg.hWnd, True)
            rect.left += tx
            rect.right -= tx
        if (is_max or is_full) and Taskbar.is_auto_hide():
            position = Taskbar.get_position(msg.hWnd)
            if position == Taskbar.LEFT:
                rect.top += Taskbar.AUTO_HIDE_THICKNESS
            elif position == Taskbar.BOTTOM:
                rect.bottom -= Taskbar.AUTO_HIDE_THICKNESS
            elif position == Taskbar.LEFT:
                rect.left += Taskbar.AUTO_HIDE_THICKNESS
            elif position == Taskbar.RIGHT:
                rect.right -= Taskbar.AUTO_HIDE_THICKNESS
        result = 0 if not msg.wParam else _wm.WVR_REDRAW
        return True, result

    def _handle_setting_change(self, msg):
        if msg.lParam:
            buf = create_unicode_buffer(256)
            _de.GlobalGetAtomNameW(msg.lParam, buf, 256)
            changed = buf.value
            if changed and "ImmersiveColorSet" in changed:
                self._on_system_theme_changed()
        return False, 0

    def _on_system_theme_changed(self):
        theme = system_theme()
        dark = theme == ThemeMode.DARK
        if win_utils.is_greater_equal_win11():
            self.window_effect.set_dark_mode(self.winId(), dark)
            self.window_effect.set_caption_color(
                self.winId(), QColor(32, 32, 32) if dark else QColor(243, 243, 243)
            )
        if is_system_border_accent_enabled():
            if dark:
                self.window_effect.set_border_accent_color(self.winId(), get_system_accent_color())
            else:
                self.window_effect.remove_border_accent_color(self.winId())
        if dark:
            self._tm.set_dark_theme()
        else:
            self._tm.set_light_theme()

    def _on_screen_changed(self):
        h_wnd = int(self.windowHandle().winId())
        _wm.SetWindowPos(
            h_wnd,
            None,
            0,
            0,
            0,
            0,
            _wm.SWP_NOMOVE | _wm.SWP_NOSIZE | _wm.SWP_FRAMECHANGED,
        )
