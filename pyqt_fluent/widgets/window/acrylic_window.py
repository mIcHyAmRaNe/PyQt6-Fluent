from ctypes.wintypes import MSG

import win32con
import win32gui
from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication

from ...tokens.theme import ThemeDefinition
from ...utils import win32_utils as win_utils
from ...utils.theme import is_dark
from ...utils.win32_utils import QT_VERSION, is_greater_equal_win10
from .frameless_window import FramelessWindow


class AcrylicWindow(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__closed_by_key = False
        self.setStyleSheet("AcrylicWindow{background:transparent}")

    @staticmethod
    def _acrylic_gradient():
        return "1A1A1A99" if is_dark() else "F2F2F299"

    def _apply_acrylic(self):
        self.window_effect.set_acrylic_effect(
            self.winId(), gradient_color=self._acrylic_gradient()
        )

    def update_frameless(self):
        stay_on_top = (
            Qt.WindowType.WindowStaysOnTopHint
            if self.windowFlags() & Qt.WindowType.WindowStaysOnTopHint
            else 0
        )
        if QT_VERSION < (6, 10, 0):
            self.setWindowFlags(Qt.WindowType.FramelessWindowHint | stay_on_top)
        else:
            self.setWindowFlags(
                Qt.WindowType.Window
                | Qt.WindowType.NoTitleBarBackgroundHint
                | stay_on_top
            )
        self.window_effect.enable_blur_behind_window(self.winId())
        self.window_effect.add_window_animation(self.winId())
        self.window_effect.add_shadow_effect(self.winId())
        self.window_effect.set_acrylic_effect(
            self.winId(), gradient_color=self._acrylic_gradient()
        )

        h_wnd = int(self.winId())
        style = win32gui.GetWindowLong(h_wnd, win32con.GWL_STYLE)
        style &= ~win32con.WS_SYSMENU
        win32gui.SetWindowLong(h_wnd, win32con.GWL_STYLE, style)

    def _on_system_theme_changed(self):
        self.window_effect.set_acrylic_effect(
            self.winId(), gradient_color=self._acrylic_gradient()
        )
        super()._on_system_theme_changed()

    def _apply_theme(self, theme: ThemeDefinition) -> None:
        self._apply_acrylic()

    def nativeEvent(self, event_type, message):
        msg = MSG.from_address(message.__int__())

        if msg.message == win32con.WM_SYSKEYDOWN and msg.wParam == win32con.VK_F4:
            self.__closed_by_key = True
            QApplication.sendEvent(self, QCloseEvent())
            return False, 0

        return super().nativeEvent(event_type, message)

    def refresh_background_blur_effect(self) -> None:
        self._apply_acrylic()

    def event(self, e: QEvent):
        if e.type() == QEvent.Type.WindowStateChange and win_utils.is_maximized(
            self.winId()
        ):
            self.refresh_background_blur_effect()
        return super().event(e)

    def closeEvent(self, e):
        if not self.__closed_by_key or QApplication.quitOnLastWindowClosed():
            self.__closed_by_key = False
            return super().closeEvent(e)
        self.__closed_by_key = False
        self.hide()
