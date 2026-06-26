from enum import Enum
from importlib.resources import files as _resources

from PyQt6.QtCore import QFile, QPointF, QRectF, Qt, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QPen
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QAbstractButton
from PyQt6.QtXml import QDomDocument

from ...tokens.theme import ThemeDefinition, ThemeManager, ThemeObserver


class ButtonState(Enum):
    NORMAL = 0
    HOVER = 1
    PRESSED = 2


class TitleBarButton(QAbstractButton, ThemeObserver):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setFixedSize(46, 32)
        self._state = ButtonState.NORMAL
        self._tm = ThemeManager.instance()
        self._tm.register_observer(self)

        self._normal_color = QColor(0, 0, 0)
        self._hover_color = QColor(0, 0, 0)
        self._pressed_color = QColor(0, 0, 0)
        self._normal_bg = QColor(0, 0, 0, 0)
        self._hover_bg = QColor(0, 0, 0, 26)
        self._pressed_bg = QColor(0, 0, 0, 51)

        self._close_hover_bg = QColor(232, 17, 35)
        self._close_pressed_bg = QColor(241, 112, 122)
        self._close_hover_fg = Qt.GlobalColor.white
        self._close_pressed_fg = Qt.GlobalColor.white

        self._apply_theme(self._tm.theme())

    def on_theme_changed(self, theme: ThemeDefinition) -> None:
        self._apply_theme(theme)

    def _apply_theme(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._normal_color = r.color("component.titlebar_button.rest")
        self._hover_color = r.color("component.titlebar_button.hover")
        self._pressed_color = r.color("component.titlebar_button.pressed")
        self._normal_bg = r.color("component.titlebar_button_bg.rest")
        self._hover_bg = r.color("component.titlebar_button_bg.hover")
        self._pressed_bg = r.color("component.titlebar_button_bg.pressed")
        self._close_hover_bg = r.color("component.close_button_bg.hover")
        self._close_pressed_bg = r.color("component.close_button_bg.pressed")
        self._close_hover_fg = r.color("component.close_button_fg.hover")
        self._close_pressed_fg = r.color("component.close_button_fg.pressed")
        self.update()

    def set_state(self, state):
        self._state = state
        self.update()

    def is_pressed(self):
        return self._state == ButtonState.PRESSED

    def get_normal_color(self):
        return self._normal_color

    def get_hover_color(self):
        return self._hover_color

    def get_pressed_color(self):
        return self._pressed_color

    def get_normal_background_color(self):
        return self._normal_bg

    def get_hover_background_color(self):
        return self._hover_bg

    def get_pressed_background_color(self):
        return self._pressed_bg

    def set_normal_color(self, color):
        self._normal_color = QColor(color)
        self.update()

    def set_hover_color(self, color):
        self._hover_color = QColor(color)
        self.update()

    def set_pressed_color(self, color):
        self._pressed_color = QColor(color)
        self.update()

    def set_normal_background_color(self, color):
        self._normal_bg = QColor(color)
        self.update()

    def set_hover_background_color(self, color):
        self._hover_bg = QColor(color)
        self.update()

    def set_pressed_background_color(self, color):
        self._pressed_bg = QColor(color)
        self.update()

    normalColor = pyqtProperty(QColor, get_normal_color, set_normal_color)
    hoverColor = pyqtProperty(QColor, get_hover_color, set_hover_color)
    pressedColor = pyqtProperty(QColor, get_pressed_color, set_pressed_color)
    normalBackgroundColor = pyqtProperty(QColor, get_normal_background_color, set_normal_background_color)
    hoverBackgroundColor = pyqtProperty(QColor, get_hover_background_color, set_hover_background_color)
    pressedBackgroundColor = pyqtProperty(QColor, get_pressed_background_color, set_pressed_background_color)

    def enterEvent(self, e):
        self.set_state(ButtonState.HOVER)
        super().enterEvent(e)

    def leaveEvent(self, e):
        self.set_state(ButtonState.NORMAL)
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() != Qt.MouseButton.LeftButton:
            return
        self.set_state(ButtonState.PRESSED)
        super().mousePressEvent(e)

    def _colors(self):
        if self._state == ButtonState.NORMAL:
            return self._normal_color, self._normal_bg
        elif self._state == ButtonState.HOVER:
            return self._hover_color, self._hover_bg
        return self._pressed_color, self._pressed_bg


class SvgTitleBarButton(TitleBarButton):
    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self._svg_dom = QDomDocument()
        self.set_icon(icon_path)

    def set_icon(self, icon_path):
        f = QFile(icon_path)
        f.open(QFile.OpenModeFlag.ReadOnly)
        self._svg_dom.setContent(f.readAll())
        f.close()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        color, bg_color = self._colors()
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())
        color = color.name()
        path_nodes = self._svg_dom.elementsByTagName("path")
        for i in range(path_nodes.length()):
            element = path_nodes.at(i).toElement()
            element.setAttribute("stroke", color)
        renderer = QSvgRenderer(self._svg_dom.toByteArray())
        renderer.render(painter, QRectF(self.rect()))


class MinimizeButton(TitleBarButton):
    def paintEvent(self, e):
        painter = QPainter(self)
        color, bg_color = self._colors()
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(18, 16, 28, 16)


class MaximizeButton(TitleBarButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_max = False

    def set_max_state(self, is_max):
        if self._is_max == is_max:
            return
        self._is_max = is_max
        self.set_state(ButtonState.NORMAL)

    def paintEvent(self, e):
        painter = QPainter(self)
        color, bg_color = self._colors()
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        r = self.devicePixelRatioF()
        painter.scale(1 / r, 1 / r)
        if not self._is_max:
            painter.drawRect(int(18 * r), int(11 * r), int(10 * r), int(10 * r))
        else:
            painter.drawRect(int(18 * r), int(13 * r), int(8 * r), int(8 * r))
            x0 = int(18 * r) + int(2 * r)
            y0 = 13 * r
            dw = int(2 * r)
            path = QPainterPath(QPointF(x0, y0))
            path.lineTo(x0, y0 - dw)
            path.lineTo(x0 + 8 * r, y0 - dw)
            path.lineTo(x0 + 8 * r, y0 - dw + 8 * r)
            path.lineTo(x0 + 8 * r - dw, y0 - dw + 8 * r)
            painter.drawPath(path)


class CloseButton(SvgTitleBarButton):
    def __init__(self, parent=None):
        icon_path = str(_resources("pyqt_fluent.resources").joinpath("icons", "close.svg"))
        super().__init__(icon_path, parent)
        self._apply_close_overrides()

    def _apply_close_overrides(self):
        self.set_hover_color(self._close_hover_fg)
        self.set_pressed_color(self._close_pressed_fg)
        self.set_hover_background_color(self._close_hover_bg)
        self.set_pressed_background_color(self._close_pressed_bg)

    def _apply_theme(self, theme: ThemeDefinition) -> None:
        super()._apply_theme(theme)
        self._apply_close_overrides()
