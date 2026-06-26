# coding:utf-8
import sys
import warnings
from ctypes import (
    POINTER,
    Structure,
    WinDLL,
    byref,
    c_bool,
    c_int,
    c_ulong,
    sizeof,
    windll,
    wintypes,
)
from ctypes.wintypes import DWORD, HWND, LPARAM, RECT, UINT
from winreg import HKEY_CURRENT_USER, KEY_READ, CloseKey, OpenKey, QueryValueEx

import win32api
import win32con
import win32gui
import win32print
from PyQt6.QtCore import QEvent, QObject, QOperatingSystemVersion, qVersion
from PyQt6.QtGui import QColor, QGuiApplication
from PyQt6.QtWidgets import QWidget
from win32comext.shell import shellcon

QT_VERSION = tuple(int(v) for v in qVersion().split("."))


def get_system_accent_color():
    """get the accent color of system

    Returns
    -------
    color: QColor
        accent color
    """
    DwmGetColorizationColor = windll.dwmapi.DwmGetColorizationColor
    DwmGetColorizationColor.restype = c_ulong
    DwmGetColorizationColor.argtypes = [POINTER(c_ulong), POINTER(c_bool)]

    color = c_ulong()
    code = DwmGetColorizationColor(byref(color), byref(c_bool()))

    if code != 0:
        warnings.warn("Unable to obtain system accent color.")
        return QColor()

    return QColor(color.value)


def is_system_border_accent_enabled():
    """Check whether the border accent is enabled"""
    if not is_greater_equal_win11():
        return False

    try:
        key = OpenKey(HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\DWM", 0, KEY_READ)
        value, _ = QueryValueEx(key, "ColorPrevalence")
        CloseKey(key)

        return bool(value)
    except:
        return False


def is_maximized(h_wnd):
    """Determine whether the window is maximized

    Parameters
    ----------
    h_wnd: int or `sip.voidptr`
        window handle
    """
    window_placement = win32gui.GetWindowPlacement(h_wnd)
    if not window_placement:
        return False

    return window_placement[1] == win32con.SW_MAXIMIZE


def is_full_screen(h_wnd):
    """Determine whether the window is full screen

    Parameters
    ----------
    h_wnd: int or `sip.voidptr`
        window handle
    """
    if not h_wnd:
        return False

    h_wnd = int(h_wnd)
    win_rect = win32gui.GetWindowRect(h_wnd)
    if not win_rect:
        return False

    monitor_info = get_monitor_info(h_wnd, win32con.MONITOR_DEFAULTTOPRIMARY)
    if not monitor_info:
        return False

    monitor_rect = monitor_info["Monitor"]
    return all(i == j for i, j in zip(win_rect, monitor_rect))


def get_monitor_info(h_wnd, dw_flags):
    """get monitor info, return `None` if failed

    Parameters
    ----------
    h_wnd: int or `sip.voidptr`
        window handle

    dw_flags: int
        Determines the return value if the window does not intersect any display monitor
    """
    monitor = win32api.MonitorFromWindow(h_wnd, dw_flags)
    if not monitor:
        return

    return win32api.GetMonitorInfo(monitor)


def get_resize_border_thickness(h_wnd, horizontal=True):
    """get resize border thickness of widget

    Parameters
    ----------
    h_wnd: int or `sip.voidptr`
        window handle

    dpiScale: bool
        whether to use dpi scale
    """
    window = find_window(h_wnd)
    if not window:
        return 0

    frame = win32con.SM_CXSIZEFRAME if horizontal else win32con.SM_CYSIZEFRAME
    result = get_system_metrics(h_wnd, frame, horizontal) + get_system_metrics(
        h_wnd, 92, horizontal
    )

    if result > 0:
        return result

    thickness = 8 if is_composition_enabled() else 4
    return round(thickness * window.devicePixelRatio())


def get_system_metrics(h_wnd, index, horizontal):
    """get system metrics"""
    if not hasattr(windll.user32, "GetSystemMetricsForDpi"):
        return win32api.GetSystemMetrics(index)

    dpi = get_dpi_for_window(h_wnd, horizontal)
    return windll.user32.GetSystemMetricsForDpi(index, dpi)


def get_dpi_for_window(h_wnd, horizontal=True):
    """get dpi for window

    Parameters
    ----------
    h_wnd: int or `sip.voidptr`
        window handle

    dpiScale: bool
        whether to use dpi scale
    """
    if hasattr(windll.user32, "GetDpiForWindow"):
        windll.user32.GetDpiForWindow.argtypes = [HWND]
        windll.user32.GetDpiForWindow.restype = UINT
        return windll.user32.GetDpiForWindow(h_wnd)

    hdc = win32gui.GetDC(h_wnd)
    if not hdc:
        return 96

    dpi_x = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSX)
    dpi_y = win32print.GetDeviceCaps(hdc, win32con.LOGPIXELSY)
    win32gui.ReleaseDC(h_wnd, hdc)
    if dpi_x > 0 and horizontal:
        return dpi_x
    elif dpi_y > 0 and not horizontal:
        return dpi_y

    return 96


def find_window(h_wnd):
    """find window by h_wnd, return `None` if not found

    Parameters
    ----------
    h_wnd: int or `sip.voidptr`
        window handle
    """
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
    """detect if dwm composition is enabled"""
    b_result = c_int(0)
    windll.dwmapi.DwmIsCompositionEnabled(byref(b_result))
    return bool(b_result.value)


def is_greater_equal_version(version):
    """determine if the windows version >= the specifics version

    Parameters
    ----------
    version: QOperatingSystemVersion
        windows version
    """
    return QOperatingSystemVersion.current() >= version


def is_greater_equal_win8_1():
    """determine if the windows version >= Win8.1"""
    return is_greater_equal_version(QOperatingSystemVersion.Windows8_1)


def is_greater_equal_win10():
    """determine if the windows version >= Win10"""
    return is_greater_equal_version(QOperatingSystemVersion.Windows10)


def is_greater_equal_win11():
    """determine if the windows version \u2265 Win10"""
    return (
        is_greater_equal_version(QOperatingSystemVersion.Windows10)
        and sys.getwindowsversion().build >= 22000
    )


def release_mouse_left_button(h_wnd, x=0, y=0):
    """release mouse left button at (x, y)

    Parameters
    ----------
    h_wnd: int or `sip.voidptr`
        window handle

    x: int
        mouse x pos

    y: int
        mouse y pos
    """
    lp = (y & 0xFFFF) << 16 | (x & 0xFFFF)
    win32api.SendMessage(int(h_wnd), win32con.WM_LBUTTONUP, 0, lp)


class APPBARDATA(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("hWnd", HWND),
        ("uCallbackMessage", UINT),
        ("uEdge", UINT),
        ("rc", RECT),
        ("lParam", LPARAM),
    ]


class Taskbar:
    LEFT = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    NO_POSITION = 4

    AUTO_HIDE_THICKNESS = 2

    @staticmethod
    def is_auto_hide():
        """detect whether the taskbar is hidden automatically"""
        appbar_data = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, RECT(0, 0, 0, 0), 0)
        taskbar_state = windll.shell32.SHAppBarMessage(
            shellcon.ABM_GETSTATE, byref(appbar_data)
        )

        return taskbar_state == shellcon.ABS_AUTOHIDE

    @classmethod
    def get_position(cls, h_wnd):
        """get the position of auto-hide task bar

        Parameters
        ----------
        h_wnd: int or `sip.voidptr`
            window handle
        """
        if is_greater_equal_win8_1():
            monitor_info = get_monitor_info(h_wnd, win32con.MONITOR_DEFAULTTONEAREST)
            if not monitor_info:
                return cls.NO_POSITION

            monitor = RECT(*monitor_info["Monitor"])
            appbar_data = APPBARDATA(sizeof(APPBARDATA), 0, 0, 0, monitor, 0)
            positions = [cls.LEFT, cls.TOP, cls.RIGHT, cls.BOTTOM]
            for position in positions:
                appbar_data.uEdge = position
                if windll.shell32.SHAppBarMessage(11, byref(appbar_data)):
                    return position

            return cls.NO_POSITION

        appbar_data = APPBARDATA(
            sizeof(APPBARDATA),
            win32gui.FindWindow("Shell_TrayWnd", None),
            0,
            0,
            RECT(0, 0, 0, 0),
            0,
        )
        if appbar_data.hWnd:
            window_monitor = win32api.MonitorFromWindow(
                h_wnd, win32con.MONITOR_DEFAULTTONEAREST
            )
            if not window_monitor:
                return cls.NO_POSITION

            taskbar_monitor = win32api.MonitorFromWindow(
                appbar_data.hWnd, win32con.MONITOR_DEFAULTTOPRIMARY
            )
            if not taskbar_monitor:
                return cls.NO_POSITION

            if taskbar_monitor == window_monitor:
                windll.shell32.SHAppBarMessage(
                    shellcon.ABM_GETTASKBARPOS, byref(appbar_data)
                )
                return appbar_data.uEdge

        return cls.NO_POSITION


class WindowsMoveResize:
    """Tool class for moving and resizing Windows window"""

    @staticmethod
    def start_system_move(window, global_pos):
        """resize window

        Parameters
        ----------
        window: QWidget
            window

        global_pos: QPoint
            the global point of mouse release event
        """
        win32gui.ReleaseCapture()
        win32api.SendMessage(
            int(window.winId()),
            win32con.WM_SYSCOMMAND,
            win32con.SC_MOVE | win32con.HTCAPTION,
            0,
        )

    @classmethod
    def star_system_resize(cls, window, global_pos, edges):
        """resize window

        Parameters
        ----------
        window: QWidget
            window

        global_pos: QPoint
            the global point of mouse release event

        edges: `Qt.Edges`
            window edges
        """
        pass

    @classmethod
    def toggle_max_state(cls, window):
        if QT_VERSION < (6, 8, 0):
            if window.isMaximized():
                window.showNormal()
            else:
                window.showMaximized()
        else:
            if window.isMaximized():
                win32gui.PostMessage(
                    int(window.winId()), win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0
                )
            else:
                win32gui.PostMessage(
                    int(window.winId()), win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0
                )

        release_mouse_left_button(window.winId())


class ScreenCaptureFilter(QObject):
    """Filter for screen capture"""

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.set_screen_capture_enabled(False)

    def eventFilter(self, watched, event):
        if watched == self.parent():
            if event.type() == QEvent.Type.WinIdChange:
                self.set_screen_capture_enabled(self.is_screen_capture_enabled)

        return super().eventFilter(watched, event)

    def set_screen_capture_enabled(self, enabled: bool):
        """Set screen capture enabled"""
        self.is_screen_capture_enabled = enabled
        WDA_NONE = 0x00000000
        WDA_EXCLUDEFROMCAPTURE = 0x00000011

        user32 = WinDLL("user32", use_last_error=True)
        SetWindowDisplayAffinity = user32.SetWindowDisplayAffinity
        SetWindowDisplayAffinity.argtypes = (wintypes.HWND, wintypes.DWORD)
        SetWindowDisplayAffinity.restype = wintypes.BOOL

        SetWindowDisplayAffinity(
            int(self.parent().winId()), WDA_NONE if enabled else WDA_EXCLUDEFROMCAPTURE
        )
