from __future__ import annotations

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty, QObject
from PyQt6.QtGui import QColor


class BackgroundColorObject(QObject):
    """Separate QObject holding the animated background colour.

    QPropertyAnimation requires a proper QObject + pyqtProperty to interpolate
    cleanly without the black-flicker that QVariantAnimation + raw QColor can
    produce.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._bg = QColor(0, 0, 0, 0)

    @pyqtProperty(QColor)
    def backgroundColor(self):
        return self._bg

    @backgroundColor.setter
    def backgroundColor(self, color: QColor):
        self._bg = color
        self.parent().update()


class BackgroundAnimationWidget:
    """Mixin — animates background colour via QPropertyAnimation on a proxy object.

    Subclasses override ``_target_bg() -> QColor``.
    Call ``_start_bg_animation()`` when the state driving ``_target_bg()``
    changes.

    The mixin sets ``_theme_applied`` to ``True`` from the outside (usually
    at the end of the subclass ``__init__``) so the very first state transition
    can skip animation and jump straight to the target.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._bg_obj = BackgroundColorObject(self)
        self._bg_ani = QPropertyAnimation(
            self._bg_obj, b"backgroundColor", self)
        self._bg_ani.setDuration(120)
        self._bg_ani.setEasingCurve(QEasingCurve.Type.OutCubic)

    def _target_bg(self) -> QColor:
        return QColor(0, 0, 0, 0)

    @property
    def _animated_bg(self) -> QColor:
        return self._bg_obj.backgroundColor

    @_animated_bg.setter
    def _animated_bg(self, color: QColor) -> None:
        self._bg_obj.backgroundColor = color
        self.update()

    def _start_bg_animation(self) -> None:
        target = self._target_bg()
        if not getattr(self, "_theme_applied", False) or not self.isVisible():
            self._bg_obj.backgroundColor = target
            self.update()
            return

        self._bg_ani.stop()
        self._bg_ani.setStartValue(self._bg_obj.backgroundColor)
        self._bg_ani.setEndValue(target)
        self._bg_ani.start()
