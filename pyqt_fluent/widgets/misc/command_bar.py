from __future__ import annotations

from collections.abc import Callable

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPainterPath, QPen, QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QSizePolicy, QWidget

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class _CommandBarButton(ThemeAwareWidget, QPushButton):
    def __init__(self, text="", icon=None, parent=None,
                 fg_color=None, hover_color=None, pressed_color=None):
        super().__init__(parent)
        self.setText(text)
        self._icon_pixmap: QPixmap | None = None
        self._icon_path = icon
        self._fg = QColor()
        self._hover = QColor()
        self._pressed = QColor()
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_hover = QColor(hover_color) if hover_color else None
        self._custom_pressed = QColor(pressed_color) if pressed_color else None
        self._hovered = False

        self.setFlat(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)
        self.setFixedHeight(36)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._fg = self._custom_fg if self._custom_fg else r.color("component.commandbar_fg")
        self._hover = self._custom_hover if self._custom_hover else r.color("component.commandbar_item_hover")
        self._pressed = self._custom_pressed if self._custom_pressed else r.color("component.commandbar_item_pressed")
        if self._icon_path:
            self._icon_pixmap = QPixmap(self._icon_path)
            if self._icon_pixmap.isNull():
                self._icon_pixmap = None
        self.update()

    def enterEvent(self, e):
        self._hovered = True
        self.update()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._hovered = False
        self.update()
        super().leaveEvent(e)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._hovered:
            painter.fillRect(self.rect(), QBrush(self._hover))

        font = QFont("Segoe UI Variable, Segoe UI, sans-serif")
        font.setPixelSize(13)
        painter.setFont(font)
        painter.setPen(self._fg)

        r = self.rect()
        text_r = QRectF(r)

        if self._icon_pixmap:
            sz = 16
            pix = self._icon_pixmap.scaled(
                sz, sz, Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            ix = r.x() + 8
            iy = r.y() + (r.height() - sz) // 2
            painter.drawPixmap(ix, iy, pix)
            text_r = QRectF(ix + sz + 6, r.y(), r.width() - (ix + sz + 6 - r.x()), r.height())

        painter.drawText(text_r, Qt.AlignmentFlag.AlignCenter, self.text())


class _Separator(QWidget):
    def __init__(self, parent=None, color=None):
        super().__init__(parent)
        self._color = QColor(color) if color else QColor(200, 200, 200)
        self.setFixedWidth(1)
        self.setFixedHeight(24)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def set_color(self, color: QColor):
        self._color = color
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.fillRect(self.rect(), self._color)


class CommandBar(ThemeAwareWidget, QWidget):
    def __init__(self, parent=None, bg_color=None, fg_color=None,
                 item_hover=None, item_pressed=None, border_color=None):
        super().__init__(parent)
        self._bg = QColor()
        self._border = QColor()
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_item_hover = QColor(item_hover) if item_hover else None
        self._custom_item_pressed = QColor(item_pressed) if item_pressed else None
        self._custom_border = QColor(border_color) if border_color else None
        self._separator_color = QColor()

        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(4, 2, 4, 2)
        self._layout.setSpacing(2)

        self.setFixedHeight(40)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._init_theme_aware()

    def add_action(self, text: str, icon: str | None = None, callback: Callable | None = None) -> _CommandBarButton:
        btn = _CommandBarButton(
            text=text, icon=icon, parent=self,
            fg_color=self._custom_fg,
            hover_color=self._custom_item_hover,
            pressed_color=self._custom_item_pressed,
        )
        if callback:
            btn.clicked.connect(callback)
        self._layout.addWidget(btn)
        return btn

    def add_separator(self):
        sep = _Separator(self, self._separator_color)
        self._layout.addWidget(sep)

    def add_stretch(self):
        self._layout.addStretch()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._bg = self._custom_bg if self._custom_bg else r.color("component.commandbar_bg")
        self._border = self._custom_border if self._custom_border else r.color("component.commandbar_border")
        self._separator_color = r.color("component.commandbar_separator")
        for i in range(self._layout.count()):
            item = self._layout.itemAt(i)
            if item and item.widget():
                if isinstance(item.widget(), _Separator):
                    item.widget().set_color(self._separator_color)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        r = 4
        path.addRoundedRect(rect, r, r)
        painter.fillPath(path, QBrush(self._bg))

        pen = QPen(self._border, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)
