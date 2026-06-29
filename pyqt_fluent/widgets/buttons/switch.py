from __future__ import annotations

from PyQt6.QtCore import Qt, QRectF, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QBrush, QPen
from PyQt6.QtWidgets import QAbstractButton, QSizePolicy

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget
from .._shared.background_animation import BackgroundAnimationWidget


class Switch(BackgroundAnimationWidget, ThemeAwareWidget, QAbstractButton):
    switch_width: int = 44
    switch_height: int = 20
    switch_thumb_size: int = 16

    def __init__(self, parent=None,
                 track_on=None, track_off=None, thumb_color=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(self.switch_width, self.switch_height)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self._track_off = QColor()
        self._track_on = QColor()
        self._thumb = QColor()
        self._custom_track_on = QColor(track_on) if track_on else None
        self._custom_track_off = QColor(track_off) if track_off else None
        self._custom_thumb = QColor(thumb_color) if thumb_color else None
        self._thumb_pos = 0.0

        self._pos_ani = QPropertyAnimation(self, b"thumb_pos", self)
        self._pos_ani.setDuration(150)
        self._pos_ani.setEasingCurve(QEasingCurve.Type.OutQuad)

        self._theme_applied = False
        self._init_theme_aware()
        self._theme_applied = True

    def _get_thumb_pos(self) -> float:
        return self._thumb_pos

    def _set_thumb_pos(self, v: float) -> None:
        self._thumb_pos = v
        self.update()

    thumb_pos = pyqtProperty(float, _get_thumb_pos, _set_thumb_pos)

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._track_off = (self._custom_track_off if self._custom_track_off
                           else r.color("component.switch_track_off"))
        self._track_on = (self._custom_track_on if self._custom_track_on
                          else r.color("component.switch_track_on"))
        self._thumb = (self._custom_thumb if self._custom_thumb
                       else r.color("component.switch_thumb"))
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

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        h = self.switch_height
        track_rect = QRectF(0, 0, self.switch_width, h)
        track_r = h / 2.0

        bg = (self._animated_bg if self._bg_ani.state() == self._bg_ani.State.Running
              else self._target_bg())

        # Track
        path = QPainterPath()
        path.addRoundedRect(track_rect, track_r, track_r)
        painter.fillPath(path, QBrush(bg))

        # Thumb
        ts = self.switch_thumb_size
        margin = (h - ts) / 2.0
        thumb_rect = QRectF(self._thumb_pos, margin, ts, ts)
        painter.setPen(Qt.PenStyle.NoPen)
        thumb_path = QPainterPath()
        thumb_path.addEllipse(thumb_rect)
        painter.fillPath(thumb_path, QBrush(self._thumb))

        # Thumb subtle shadow/border
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = QPen(QColor(0, 0, 0, 20), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawEllipse(thumb_rect)
