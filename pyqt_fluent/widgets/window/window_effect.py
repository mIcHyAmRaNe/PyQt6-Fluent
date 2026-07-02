import warnings
from ctypes import POINTER, WinDLL, byref, c_int, pointer, sizeof
from ctypes.wintypes import DWORD
from platform import version

from PyQt6.QtGui import QColor
from win32more.Windows.Win32.Graphics.Dwm import (
    DWM_BB_ENABLE,
    DWM_BLURBEHIND,
    DWMNCRP_DISABLED,
    DWMNCRP_ENABLED,
    DWMWA_BORDER_COLOR,
    DWMWA_CAPTION_COLOR,
    DWMWA_NCRENDERING_POLICY,
    DWMWA_SYSTEMBACKDROP_TYPE,
    DWMWA_USE_IMMERSIVE_DARK_MODE,
)
from win32more.Windows.Win32.Graphics.Dwm import (
    DwmEnableBlurBehindWindow as _DwmEnableBlurBehindWindow,
)
from win32more.Windows.Win32.Graphics.Dwm import (
    DwmExtendFrameIntoClientArea as _DwmExtendFrameIntoClientArea,
)
from win32more.Windows.Win32.Graphics.Dwm import (
    DwmSetWindowAttribute as _DwmSetWindowAttribute,
)
from win32more.Windows.Win32.UI import WindowsAndMessaging as _wm
from win32more.Windows.Win32.UI.Controls import MARGINS as _MARGINS

from ...utils.win32_utils import (
    is_composition_enabled,
    is_greater_equal_win10,
    is_greater_equal_win11,
)
from .c_structures import (
    ACCENT_POLICY,
    ACCENT_STATE,
    WINDOWCOMPOSITIONATTRIB,
    WINDOWCOMPOSITIONATTRIBDATA,
)


class WindowsWindowEffect:
    def __init__(self, window):
        self.window = window

        # SetWindowCompositionAttribute is undocumented — keep ctypes
        self._user32 = WinDLL("user32")
        self.SetWindowCompositionAttribute = self._user32.SetWindowCompositionAttribute
        self.SetWindowCompositionAttribute.restype = c_int
        self.SetWindowCompositionAttribute.argtypes = [
            c_int, POINTER(WINDOWCOMPOSITIONATTRIBDATA)
        ]

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
        _DwmSetWindowAttribute(h_wnd, DWMWA_BORDER_COLOR, byref(color_ref), 4)

    def set_dark_mode(self, h_wnd, is_dark: bool):
        if not is_greater_equal_win11():
            return
        h_wnd = int(h_wnd)
        _DwmSetWindowAttribute(
            h_wnd, DWMWA_USE_IMMERSIVE_DARK_MODE, byref(c_int(1 if is_dark else 0)), 4
        )

    def remove_border_accent_color(self, h_wnd):
        if not is_greater_equal_win11():
            return
        h_wnd = int(h_wnd)
        _DwmSetWindowAttribute(h_wnd, DWMWA_BORDER_COLOR, byref(DWORD(0xFFFFFFFF)), 4)

    def set_caption_color(self, h_wnd, color: QColor):
        if not is_greater_equal_win11():
            return
        h_wnd = int(h_wnd)
        color_ref = DWORD(color.red() | (color.green() << 8) | (color.blue() << 16))
        _DwmSetWindowAttribute(h_wnd, DWMWA_CAPTION_COLOR, byref(color_ref), 4)

    def set_mica_effect(self, h_wnd, is_dark_mode=False, is_alt=False):
        if not is_greater_equal_win11():
            warnings.warn("The mica effect is only available on Win11")
            return
        h_wnd = int(h_wnd)
        margins = _MARGINS(16777215, 16777215, 0, 0)
        _DwmExtendFrameIntoClientArea(h_wnd, byref(margins))
        self.win_comp_attr_data.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_ACCENT_POLICY.value
        self.accent_policy.AccentState = ACCENT_STATE.ACCENT_ENABLE_HOSTBACKDROP.value
        self.SetWindowCompositionAttribute(h_wnd, pointer(self.win_comp_attr_data))
        if is_dark_mode:
            self.win_comp_attr_data.Attribute = WINDOWCOMPOSITIONATTRIB.WCA_USEDARKMODECOLORS.value
            self.SetWindowCompositionAttribute(h_wnd, pointer(self.win_comp_attr_data))
        if int(version().split(".")[2]) < 22523:
            _DwmSetWindowAttribute(h_wnd, 1029, byref(c_int(1)), 4)
        else:
            _DwmSetWindowAttribute(
                h_wnd, DWMWA_SYSTEMBACKDROP_TYPE,
                byref(c_int(4 if is_alt else 2)), 4,
            )
        _DwmSetWindowAttribute(
            h_wnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
            byref(c_int(1 * is_dark_mode)), 4,
        )

    def remove_background_effect(self, h_wnd):
        h_wnd = int(h_wnd)
        self.accent_policy.AccentState = ACCENT_STATE.ACCENT_DISABLED.value
        self.SetWindowCompositionAttribute(h_wnd, pointer(self.win_comp_attr_data))

    def add_shadow_effect(self, h_wnd):
        if not is_composition_enabled():
            return
        h_wnd = int(h_wnd)
        margins = _MARGINS(-1, -1, -1, -1)
        _DwmExtendFrameIntoClientArea(h_wnd, byref(margins))

    def add_menu_shadow_effect(self, h_wnd):
        if not is_composition_enabled():
            return
        h_wnd = int(h_wnd)
        _DwmSetWindowAttribute(
            h_wnd, DWMWA_NCRENDERING_POLICY,
            byref(c_int(DWMNCRP_ENABLED)), 4,
        )
        margins = _MARGINS(-1, -1, -1, -1)
        _DwmExtendFrameIntoClientArea(h_wnd, byref(margins))

    def remove_shadow_effect(self, h_wnd):
        h_wnd = int(h_wnd)
        _DwmSetWindowAttribute(
            h_wnd, DWMWA_NCRENDERING_POLICY,
            byref(c_int(DWMNCRP_DISABLED)), 4,
        )

    def add_window_animation(self, h_wnd):
        h_wnd = int(h_wnd)
        style = _wm.GetWindowLongW(h_wnd, _wm.GWL_STYLE)
        _wm.SetWindowLongW(
            h_wnd, _wm.GWL_STYLE,
            style | _wm.WS_MINIMIZEBOX | _wm.WS_MAXIMIZEBOX
            | _wm.WS_CAPTION | _wm.CS_DBLCLKS | _wm.WS_THICKFRAME,
        )

    def disable_maximize_button(self, h_wnd):
        h_wnd = int(h_wnd)
        style = _wm.GetWindowLongW(h_wnd, _wm.GWL_STYLE)
        _wm.SetWindowLongW(h_wnd, _wm.GWL_STYLE, style & ~_wm.WS_MAXIMIZEBOX)

    def enable_blur_behind_window(self, h_wnd):
        blur_behind = DWM_BLURBEHIND()
        blur_behind.dwFlags = DWM_BB_ENABLE
        blur_behind.fEnable = True
        blur_behind.hRgnBlur = 0
        blur_behind.fTransitionOnMaximized = False
        _DwmEnableBlurBehindWindow(int(h_wnd), byref(blur_behind))

    def remove_window_animation(self, h_wnd):
        h_wnd = int(h_wnd)
        style = _wm.GetWindowLongW(h_wnd, _wm.GWL_STYLE)
        style &= ~_wm.WS_MINIMIZEBOX
        style &= ~_wm.WS_MAXIMIZEBOX
        style &= ~_wm.WS_CAPTION
        style &= ~_wm.WS_THICKFRAME
        _wm.SetWindowLongW(h_wnd, _wm.GWL_STYLE, style)
        _wm.SetWindowPos(
            h_wnd, None, 0, 0, 0, 0,
            _wm.SWP_NOMOVE | _wm.SWP_NOSIZE | _wm.SWP_NOZORDER | _wm.SWP_FRAMECHANGED,
        )

    def disable_blur_behind_window(self, h_wnd):
        blur_behind = DWM_BLURBEHIND()
        blur_behind.dwFlags = DWM_BB_ENABLE
        blur_behind.fEnable = False
        blur_behind.hRgnBlur = 0
        blur_behind.fTransitionOnMaximized = False
        _DwmEnableBlurBehindWindow(int(h_wnd), byref(blur_behind))
