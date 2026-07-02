import sys
import warnings
from ctypes import byref, c_bool, c_int, c_ulong
from winreg import HKEY_CURRENT_USER, KEY_READ, CloseKey, OpenKey, QueryValueEx

from PyQt6.QtCore import QEvent, QObject, QOperatingSystemVersion, qVersion
from PyQt6.QtGui import QColor, QGuiApplication
from PyQt6.QtWidgets import QWidget
from win32more.Windows.Win32.Graphics import Gdi as _gdi
from win32more.Windows.Win32.Graphics.Dwm import (
    DwmGetColorizationColor as _DwmGetColorizationColor,
)
from win32more.Windows.Win32.Graphics.Dwm import (
    DwmIsCompositionEnabled as _DwmIsCompositionEnabled,
)
from win32more.Windows.Win32.UI import HiDpi as _hidpi
from win32more.Windows.Win32.UI import Shell as _shell
from win32more.Windows.Win32.UI import WindowsAndMessaging as _wm
from win32more.Windows.Win32.UI.Input import KeyboardAndMouse as _km

QT_VERSION = tuple(int(v) for v in qVersion().split("."))


def get_system_accent_color():
    color = c_ulong()
    code = _DwmGetColorizationColor(byref(color), byref(c_bool()))
    if code != 0:
        warnings.warn("Unable to obtain system accent color.")
        return QColor()
    return QColor(color.value)


def is_system_border_accent_enabled():
    if not is_greater_equal_win11():
        return False
    try:
        key = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\DWM", 0, KEY_READ)
        value, _ = QueryValueEx(key, "ColorPrevalence")
        CloseKey(key)
        return bool(value)
    except Exception:
        return False


def is_maximized(h_wnd):
    h_wnd = int(h_wnd)
    wp = _wm.WINDOWPLACEMENT()
    wp.length = 44
    result = _wm.GetWindowPlacement(h_wnd, wp)
    if not result:
        return False
    return wp.showCmd == _wm.SW_MAXIMIZE


def is_full_screen(h_wnd):
    if not h_wnd:
        return False
    h_wnd = int(h_wnd)
    from win32more.Windows.Win32.Foundation import RECT as _MRECT
    win_rect = _MRECT()
    result = _wm.GetWindowRect(h_wnd, win_rect)
    if not result:
        return False
    monitor_info = get_monitor_info(h_wnd, _gdi.MONITOR_DEFAULTTOPRIMARY)
    if not monitor_info:
        return False
    monitor_rect = monitor_info["Monitor"]
    return (
        win_rect.left == monitor_rect.left
        and win_rect.top == monitor_rect.top
        and win_rect.right == monitor_rect.right
        and win_rect.bottom == monitor_rect.bottom
    )


def get_monitor_info(h_wnd, dw_flags):
    h_wnd = int(h_wnd)
    monitor = _gdi.MonitorFromWindow(h_wnd, dw_flags)
    if not monitor:
        return
    from win32more.Windows.Win32.Foundation import RECT as _MRECT
    from win32more.Windows.Win32.Graphics.Gdi import MONITORINFO
    mi = MONITORINFO()
    mi.cbSize = 40
    result = _gdi.GetMonitorInfoW(monitor, mi)
    if not result:
        return
    return {
        "Monitor": _MRECT(
            mi.rcMonitor.left,
            mi.rcMonitor.top,
            mi.rcMonitor.right,
            mi.rcMonitor.bottom,
        ),
        "Work": _MRECT(
            mi.rcWork.left,
            mi.rcWork.top,
            mi.rcWork.right,
            mi.rcWork.bottom,
        ),
        "dwFlags": mi.dwFlags,
    }


def get_resize_border_thickness(h_wnd, horizontal=True):
    window = find_window(h_wnd)
    if not window:
        return 0
    frame = _wm.SM_CXSIZEFRAME if horizontal else _wm.SM_CYSIZEFRAME
    result = get_system_metrics(h_wnd, frame, horizontal) + get_system_metrics(
        h_wnd, _wm.SM_CXPADDEDBORDER, horizontal
    )
    if result > 0:
        return result
    thickness = 8 if is_composition_enabled() else 4
    return round(thickness * window.devicePixelRatio())


def get_system_metrics(h_wnd, index, horizontal):
    dpi = get_dpi_for_window(h_wnd, horizontal)
    return _hidpi.GetSystemMetricsForDpi(index, dpi)


def get_dpi_for_window(h_wnd, horizontal=True):
    hdc = _gdi.GetDC(int(h_wnd))
    if not hdc:
        return 96
    dpi_x = _gdi.GetDeviceCaps(hdc, _gdi.LOGPIXELSX)
    dpi_y = _gdi.GetDeviceCaps(hdc, _gdi.LOGPIXELSY)
    _gdi.ReleaseDC(int(h_wnd), hdc)
    if dpi_x > 0 and horizontal:
        return dpi_x
    elif dpi_y > 0 and not horizontal:
        return dpi_y
    return 96


def find_window(h_wnd):
    if not h_wnd:
        return
    windows = QGuiApplication.topLevelWindows()
    if not windows:
        return
    h_wnd = int(h_wnd)
    for window in windows:
        if window and int(window.winId()) == h_wnd:
            return window


def is_composition_enabled():
    result = c_int(0)
    _DwmIsCompositionEnabled(byref(result))
    return bool(result.value)


def is_greater_equal_version(version):
    return QOperatingSystemVersion.current() >= version


def is_greater_equal_win8_1():
    return is_greater_equal_version(QOperatingSystemVersion.Windows8_1)


def is_greater_equal_win10():
    return is_greater_equal_version(QOperatingSystemVersion.Windows10)


def is_greater_equal_win11():
    return (
        is_greater_equal_version(QOperatingSystemVersion.Windows10)
        and sys.getwindowsversion().build >= 22000
    )


def release_mouse_left_button(h_wnd, x=0, y=0):
    lp = (y & 0xFFFF) << 16 | (x & 0xFFFF)
    _wm.SendMessage(int(h_wnd), _wm.WM_LBUTTONUP, 0, lp)


class Taskbar:
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    NO_POSITION = 4
    AUTO_HIDE_THICKNESS = 2

    @staticmethod
    def is_auto_hide():
        appbar_data = _shell.APPBARDATA()
        appbar_data.cbSize = 48
        taskbar_state = _shell.SHAppBarMessage(_shell.ABM_GETSTATE, appbar_data)
        return taskbar_state == _shell.ABS_AUTOHIDE

    @classmethod
    def get_position(cls, h_wnd):
        if is_greater_equal_win8_1():
            monitor_info = get_monitor_info(h_wnd, _gdi.MONITOR_DEFAULTTONEAREST)
            if not monitor_info:
                return cls.NO_POSITION
            monitor = monitor_info["Monitor"]
            appbar_data = _shell.APPBARDATA()
            appbar_data.cbSize = 48
            appbar_data.rc = monitor
            for position in (cls.LEFT, cls.TOP, cls.RIGHT, cls.BOTTOM):
                appbar_data.uEdge = position
                if _shell.SHAppBarMessage(11, appbar_data):
                    return position
            return cls.NO_POSITION

        tray_hwnd = _wm.FindWindowW("Shell_TrayWnd", None)
        appbar_data = _shell.APPBARDATA()
        appbar_data.cbSize = 48
        appbar_data.hWnd = tray_hwnd
        if appbar_data.hWnd:
            window_monitor = _gdi.MonitorFromWindow(h_wnd, _gdi.MONITOR_DEFAULTTONEAREST)
            if not window_monitor:
                return cls.NO_POSITION
            taskbar_monitor = _gdi.MonitorFromWindow(appbar_data.hWnd, _gdi.MONITOR_DEFAULTTOPRIMARY)
            if not taskbar_monitor:
                return cls.NO_POSITION
            if taskbar_monitor == window_monitor:
                _shell.SHAppBarMessage(_shell.ABM_GETTASKBARPOS, appbar_data)
                return appbar_data.uEdge
        return cls.NO_POSITION


class WindowsMoveResize:
    @staticmethod
    def start_system_move(window, global_pos):
        _km.ReleaseCapture()
        _wm.SendMessage(
            int(window.winId()),
            _wm.WM_SYSCOMMAND,
            _wm.SC_MOVE | _wm.HTCAPTION,
            0,
        )

    @staticmethod
    def star_system_resize(window, global_pos, edges):
        pass

    @staticmethod
    def toggle_max_state(window):
        if QT_VERSION < (6, 8, 0):
            if window.isMaximized():
                window.showNormal()
            else:
                window.showMaximized()
        else:
            if window.isMaximized():
                _wm.PostMessage(
                    int(window.winId()), _wm.WM_SYSCOMMAND, _wm.SC_RESTORE, 0
                )
            else:
                _wm.PostMessage(
                    int(window.winId()), _wm.WM_SYSCOMMAND, _wm.SC_MAXIMIZE, 0
                )
        release_mouse_left_button(window.winId())


class ScreenCaptureFilter(QObject):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.set_screen_capture_enabled(False)

    def eventFilter(self, watched, event):
        if watched == self.parent():
            if event.type() == QEvent.Type.WinIdChange:
                self.set_screen_capture_enabled(self.is_screen_capture_enabled)
        return super().eventFilter(watched, event)

    def set_screen_capture_enabled(self, enabled: bool):
        self.is_screen_capture_enabled = enabled
        WDA_NONE = 0x00000000
        WDA_EXCLUDEFROMCAPTURE = 0x00000011
        _wm.SetWindowDisplayAffinity(
            int(self.parent().winId()),
            WDA_NONE if enabled else WDA_EXCLUDEFROMCAPTURE,
        )
