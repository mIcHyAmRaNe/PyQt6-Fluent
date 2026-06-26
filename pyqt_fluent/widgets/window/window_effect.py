# coding:utf-8
import warnings
from ctypes import POINTER, WinDLL, byref, c_bool, c_int, pointer, sizeof
from ctypes.wintypes import DWORD, LONG, LPCVOID
from platform import version

import win32con
import win32gui
from PyQt6.QtGui import QColor

from .c_structures import (
    ACCENT_POLICY,
    ACCENT_STATE,
    DWM_BLURBEHIND,
    DWMNCRENDERINGPOLICY,
    DWMWINDOWATTRIBUTE,
    MARGINS,
    WINDOWCOMPOSITIONATTRIB,
    WINDOWCOMPOSITIONATTRIBDATA,
)
from .platform.win32 import is_composition_enabled, is_greater_equal_win10, is_greater_equal_win11


class WindowsWindowEffect:
    def __init__(self, window):
        self.window = window
        self.user32 = WinDLL("user32")
        self.dwmapi = WinDLL("dwmapi")
        self.SetWindowCompositionAttribute = self.user32.SetWindowCompositionAttribute
        self.DwmExtendFrameIntoClientArea = self.dwmapi.DwmExtendFrameIntoClientArea
        self.DwmEnableBlurBehindWindow = self.dwmapi.DwmEnableBlurBehindWindow
        self.DwmSetWindowAttribute = self.dwmapi.DwmSetWindowAttribute

        self.SetWindowCompositionAttribute.restype = c_bool
        self.DwmExtendFrameIntoClientArea.restype = LONG
        self.DwmEnableBlurBehindWindow.restype = LONG
        self.DwmSetWindowAttribute.restype = LONG
        self.SetWindowCompositionAttribute.argtypes = [c_int, POINTER(WINDOWCOMPOSITIONATTRIBDATA)]
        self.DwmSetWindowAttribute.argtypes = [c_int, DWORD, LPCVOID, DWORD]
        self.DwmExtendFrameIntoClientArea.argtypes = [c_int, POINTER(MARGINS)]
        self.DwmEnableBlurBehindWindow.argtypes = [c_int, POINTER(DWM_BLURBEHIND)]

        self.accent_policy = ACCENT_POLICY()
        self.win_comp_attr_data = WINDOWCOMPOSITIONATTRIBDATA()
        self.win_comp_attr_data.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        self.win_comp_attr_data.SizeOfData = sizeof(self.accent_policy)
        self.win_comp_attr_data.Data = pointer(self.accent_policy)

    def set_acrylic_effect(self, h_wnd, gradient_color="F2F2F299", enable_shadow=True, animation_id=0):
        if not is_greater_equal_win10():
            warnings.warn("The acrylic effect is only available on Win10+")
            return
        h_wnd = int(h_wnd)
        gradient_color = "".join(gradient_color[i : i + 2] for i in range(6, -1, -2))
        gradient_color = DWORD(int(gradient_color, base=16))
        animation_id = DWORD(animation_id)
        accent_flags = DWORD(0x20 | 0x40 | 0x80 | 0x100) if enable_shadow else DWORD(0)
        self.accent_policy.AccentState = ACCENT_STATE.ACCENT_ENABLE_ACRYLICBLURBEHIND.value
        self.accent_policy.GradientColor = gradient_color
        self.accent_policy.AccentFlags = accent_flags
        self.accent_policy.AnimationId = animation_id
        self.win_comp_attr_data.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        self.SetWindowCompositionAttribute(h_wnd, pointer(self.win_comp_attr_data))

    def set_border_accent_color(self, h_wnd, color: QColor):
        if not is_greater_equal_win11():
            return
        h_wnd = int(h_wnd)
        color_ref = DWORD(color.red() | (color.green() << 8) | (color.blue() << 16))
        self.DwmSetWindowAttribute(
            h_wnd, DWMWINDOWATTRIBUTE.DWMWA_BORDER_COLOR.value, byref(color_ref), 4
        )

    def set_dark_mode(self, h_wnd, is_dark: bool):
        if not is_greater_equal_win11():
            return
        h_wnd = int(h_wnd)
        self.DwmSetWindowAttribute(
            h_wnd,
            DWMWINDOWATTRIBUTE.DWMWA_USE_IMMERSIVE_DARK_MODE.value,
            byref(c_int(1 if is_dark else 0)),
            4,
        )

    def remove_border_accent_color(self, h_wnd):
        if not is_greater_equal_win11():
            return
        h_wnd = int(h_wnd)
        self.DwmSetWindowAttribute(
            h_wnd, DWMWINDOWATTRIBUTE.DWMWA_BORDER_COLOR.value, byref(DWORD(0xFFFFFFFF)), 4
        )

    def set_caption_color(self, h_wnd, color: QColor):
        if not is_greater_equal_win11():
            return
        h_wnd = int(h_wnd)
        color_ref = DWORD(color.red() | (color.green() << 8) | (color.blue() << 16))
        self.DwmSetWindowAttribute(
            h_wnd, DWMWINDOWATTRIBUTE.DWMWA_CAPTION_COLOR.value, byref(color_ref), 4
        )

    def set_mica_effect(self, h_wnd, is_dark_mode=False, is_alt=False):
        if not is_greater_equal_win11():
            warnings.warn("The mica effect is only available on Win11")
            return
        h_wnd = int(h_wnd)
        margins = MARGINS(16777215, 16777215, 0, 0)
        self.DwmExtendFrameIntoClientArea(h_wnd, byref(margins))
        self.win_comp_attr_data.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        self.accent_policy.AccentState = ACCENT_STATE.ACCENT_ENABLE_HOSTBACKDROP.value
        self.SetWindowCompositionAttribute(h_wnd, pointer(self.win_comp_attr_data))
        if is_dark_mode:
            self.win_comp_attr_data.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_USEDARKMODECOLORS.value
            self.SetWindowCompositionAttribute(h_wnd, pointer(self.win_comp_attr_data))
        if int(version().split(".")[2]) < 22523:
            self.DwmSetWindowAttribute(h_wnd, 1029, byref(c_int(1)), 4)
        else:
            self.DwmSetWindowAttribute(
                h_wnd,
                DWMWINDOWATTRIBUTE.DWMWA_SYSTEMBACKDROP_TYPE.value,
                byref(c_int(4 if is_alt else 2)),
                4,
            )
        self.DwmSetWindowAttribute(
            h_wnd,
            DWMWINDOWATTRIBUTE.DWMWA_USE_IMMERSIVE_DARK_MODE.value,
            byref(c_int(1 * is_dark_mode)),
            4,
        )

    def remove_background_effect(self, h_wnd):
        h_wnd = int(h_wnd)
        self.accent_policy.AccentState = ACCENT_STATE.ACCENT_DISABLED.value
        self.SetWindowCompositionAttribute(h_wnd, pointer(self.win_comp_attr_data))

    def add_shadow_effect(self, h_wnd):
        if not is_composition_enabled():
            return
        h_wnd = int(h_wnd)
        margins = MARGINS(-1, -1, -1, -1)
        self.DwmExtendFrameIntoClientArea(h_wnd, byref(margins))

    def add_menu_shadow_effect(self, h_wnd):
        if not is_composition_enabled():
            return
        h_wnd = int(h_wnd)
        self.DwmSetWindowAttribute(
            h_wnd,
            DWMWINDOWATTRIBUTE.DWMWA_NCRENDERING_POLICY.value,
            byref(c_int(DWMNCRENDERINGPOLICY.DWMNCRP_ENABLED.value)),
            4,
        )
        margins = MARGINS(-1, -1, -1, -1)
        self.DwmExtendFrameIntoClientArea(h_wnd, byref(margins))

    def remove_shadow_effect(self, h_wnd):
        h_wnd = int(h_wnd)
        self.DwmSetWindowAttribute(
            h_wnd,
            DWMWINDOWATTRIBUTE.DWMWA_NCRENDERING_POLICY.value,
            byref(c_int(DWMNCRENDERINGPOLICY.DWMNCRP_DISABLED.value)),
            4,
        )

    def add_window_animation(self, h_wnd):
        h_wnd = int(h_wnd)
        style = win32gui.GetWindowLong(h_wnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(
            h_wnd,
            win32con.GWL_STYLE,
            style
            | win32con.WS_MINIMIZEBOX
            | win32con.WS_MAXIMIZEBOX
            | win32con.WS_CAPTION
            | win32con.CS_DBLCLKS
            | win32con.WS_THICKFRAME,
        )

    def disable_maximize_button(self, h_wnd):
        h_wnd = int(h_wnd)
        style = win32gui.GetWindowLong(h_wnd, win32con.GWL_STYLE)
        win32gui.SetWindowLong(h_wnd, win32con.GWL_STYLE, style & ~win32con.WS_MAXIMIZEBOX)

    def enable_blur_behind_window(self, h_wnd):
        blur_behind = DWM_BLURBEHIND(1, True, 0, False)
        self.DwmEnableBlurBehindWindow(int(h_wnd), byref(blur_behind))

    def remove_window_animation(self, h_wnd):
        h_wnd = int(h_wnd)
        style = win32gui.GetWindowLong(h_wnd, win32con.GWL_STYLE)
        style &= ~win32con.WS_MINIMIZEBOX
        style &= ~win32con.WS_MAXIMIZEBOX
        style &= ~win32con.WS_CAPTION
        style &= ~win32con.WS_THICKFRAME
        win32gui.SetWindowLong(h_wnd, win32con.GWL_STYLE, style)
        win32gui.SetWindowPos(
            h_wnd,
            None,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE
            | win32con.SWP_NOSIZE
            | win32con.SWP_NOZORDER
            | win32con.SWP_FRAMECHANGED,
        )

    def disable_blur_behind_window(self, h_wnd):
        blur_behind = DWM_BLURBEHIND(1, False, 0, False)
        self.DwmEnableBlurBehindWindow(int(h_wnd), byref(blur_behind))
