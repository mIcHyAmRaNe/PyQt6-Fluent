from __future__ import annotations

from PyQt6.QtCore import QPropertyAnimation, QRectF, Qt, pyqtProperty
from PyQt6.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import QAbstractButton, QSizePolicy

from ...tokens.theme import ThemeDefinition
from ...utils.animation import winui_easing
from .._shared.background_animation import BackgroundAnimationWidget
from .._shared.theme_aware import ThemeAwareWidget


class Switch(BackgroundAnimationWidget, ThemeAwareWidget, QAbstractButton):
    switch_width: int = 40
    switch_height: int = 20
    switch_thumb_size: int = 16

    def __init__(self, parent=None, track_on=None, track_off=None, thumb_color=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(self.switch_width, self.switch_height)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Track colors
        self._track_off = QColor()
        self._track_on = QColor()
        self._track_off_border = QColor()
        self._track_hovered = QColor()
        self._track_disabled = QColor()
        self._border_disabled = QColor()
        # Thumb colors
        self._thumb_off = QColor()
        self._thumb_on = QColor()
        self._thumb_disabled = QColor()

        self._custom_track_on = QColor(track_on) if track_on else None
        self._custom_track_off = QColor(track_off) if track_off else None
        self._custom_thumb = QColor(thumb_color) if thumb_color else None

        self._is_hovered = False

        self._thumb_pos = 0.0
        self._thumb_scale = 0.6  # normal: 6/10

        self._pos_ani = QPropertyAnimation(self, b"thumb_pos", self)
        self._pos_ani.setDuration(167)
        self._pos_ani.setEasingCurve(winui_easing())

        self._scale_ani = QPropertyAnimation(self, b"thumb_scale", self)
        self._scale_ani.setDuration(167)
        self._scale_ani.setEasingCurve(winui_easing())

        self._theme_applied = False
        self._init_theme_aware()
        self._theme_applied = True

    def _get_thumb_pos(self) -> float:
        return self._thumb_pos

    def _set_thumb_pos(self, v: float) -> None:
        self._thumb_pos = v
        self.update()

    thumb_pos = pyqtProperty(float, _get_thumb_pos, _set_thumb_pos)

    def _get_thumb_scale(self) -> float:
        return self._thumb_scale

    def _set_thumb_scale(self, v: float) -> None:
        self._thumb_scale = v
        self.update()

    thumb_scale = pyqtProperty(float, _get_thumb_scale, _set_thumb_scale)

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        if self._custom_track_off:
            self._track_off = QColor(self._custom_track_off)
            self._track_off_border = QColor(self._custom_track_off)
        else:
            self._track_off = r.color("palette.switch_track_off")
            self._track_off_border = r.color("palette.switch_track_off_border")
            self._track_hovered = r.color("palette.switch_track_hovered")
            self._track_disabled = r.color("palette.switch_track_disabled")
            self._border_disabled = r.color("palette.switch_border_disabled")
        self._track_on = (
            self._custom_track_on if self._custom_track_on else r.color("semantic.accent")
        )
        if self._custom_thumb:
            self._thumb_off = QColor(self._custom_thumb)
            self._thumb_on = QColor(self._custom_thumb)
            self._thumb_disabled = QColor(self._custom_thumb)
        else:
            self._thumb_off = r.color("palette.switch_thumb_off")
            self._thumb_on = r.color("palette.switch_thumb_checked")
            self._thumb_disabled = r.color("palette.switch_thumb_disabled")
        self._bg_ani.stop()
        self._animated_bg = self._target_bg()
        self.update()

    def _target_bg(self) -> QColor:
        return self._track_on if self.isChecked() else self._track_off

    def resizeEvent(self, e):
        super().resizeEvent(e)
        margin = (self.switch_height - self.switch_thumb_size) // 2
        max_x = self.switch_width - self.switch_thumb_size - margin
        target = max_x if self.isChecked() else margin
        self._thumb_pos = float(target)
        self.update()

    def nextCheckState(self):
        super().nextCheckState()

        margin = (self.switch_height - self.switch_thumb_size) // 2
        max_x = self.switch_width - self.switch_thumb_size - margin
        target = max_x if self.isChecked() else margin

        self._pos_ani.stop()
        self._pos_ani.setStartValue(self._thumb_pos)
        self._pos_ani.setEndValue(float(target))
        self._pos_ani.start()

        self._start_bg_animation()

    def enterEvent(self, e):
        super().enterEvent(e)
        self._is_hovered = True
        self.update()
        self._scale_ani.stop()
        self._scale_ani.setStartValue(self._thumb_scale)
        self._scale_ani.setEndValue(0.7)  # hovered: 7/10
        self._scale_ani.start()

    def leaveEvent(self, e):
        super().leaveEvent(e)
        self._is_hovered = False
        self.update()
        self._scale_ani.stop()
        self._scale_ani.setStartValue(self._thumb_scale)
        self._scale_ani.setEndValue(0.6)  # normal: 6/10
        self._scale_ani.start()

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.MouseButton.LeftButton:
            self._scale_ani.stop()
            self._scale_ani.setStartValue(self._thumb_scale)
            self._scale_ani.setEndValue(0.5)  # pressed: 5/10
            self._scale_ani.start()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        if e.button() == Qt.MouseButton.LeftButton:
            target = 0.7 if self.rect().contains(e.pos()) else 0.6
            self._scale_ani.stop()
            self._scale_ani.setStartValue(self._thumb_scale)
            self._scale_ani.setEndValue(target)
            self._scale_ani.start()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        h = self.switch_height
        track_rect = QRectF(0, 0, self.switch_width, h)
        track_r = h / 2.0
        is_checked = self.isChecked()
        is_disabled = not self.isEnabled()

        # --- Track background ---
        if is_disabled:
            bg = self._track_disabled
        elif is_checked:
            bg = self._track_on
        elif self._is_hovered:
            bg = self._track_hovered
        else:
            bg = (
                self._animated_bg
                if self._bg_ani.state() == self._bg_ani.State.Running
                else self._track_off
            )

        track_path = QPainterPath()
        track_path.addRoundedRect(track_rect, track_r, track_r)
        painter.fillPath(track_path, QBrush(bg))

        # --- Track border (always 1px) ---
        if is_disabled:
            border_color = self._border_disabled
        elif is_checked:
            border_color = self._track_on
        else:
            border_color = self._track_off_border

        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(border_color, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawRoundedRect(track_rect, track_r, track_r)

        # --- Thumb ---
        ts = self.switch_thumb_size
        margin = (h - ts) / 2.0
        cx = self._thumb_pos + ts / 2.0
        cy = h / 2.0
        scaled_ts = ts * self._thumb_scale
        thumb_rect = QRectF(cx - scaled_ts / 2.0, cy - scaled_ts / 2.0, scaled_ts, scaled_ts)

        if is_disabled:
            dot_color = self._thumb_disabled
        elif is_checked:
            dot_color = self._thumb_on
        else:
            dot_color = self._thumb_off

        painter.setPen(Qt.PenStyle.NoPen)
        thumb_path = QPainterPath()
        thumb_path.addEllipse(thumb_rect)
        painter.fillPath(thumb_path, QBrush(dot_color))
