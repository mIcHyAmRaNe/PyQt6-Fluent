from __future__ import annotations

from enum import Enum

from PyQt6.QtCore import QPointF, QRectF, QSize, Qt
from PyQt6.QtGui import QBrush, QColor, QFontMetrics, QLinearGradient, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import QAbstractButton

from ...tokens.theme import ThemeDefinition
from .._shared.background_animation import BackgroundAnimationWidget
from .._shared.focus_ring import FocusRing
from .._shared.ripple import RippleEffect
from .._shared.theme_aware import ThemeAwareWidget
from .._shared.translate_animation import TranslateYAnimation


class _ButtonState(Enum):
    NORMAL = 0
    HOVER = 1
    PRESSED = 2


_DISABLED_OPACITY = 0.4


class ButtonBase(
    BackgroundAnimationWidget,
    TranslateYAnimation,
    ThemeAwareWidget,
    QAbstractButton,
):
    """Base for all button variants.

    Subclasses set ``control_tokens_key`` (e.g. ``"button_standard"``)
    and override ``_draw_indicator(painter)``.
    """

    control_tokens_key: str = ""
    fg_ref: str = ""
    border_ref: str = ""
    border_accent_ref: str = ""

    def __init__(self, parent=None):
        super().__init__(parent)

        self._state = _ButtonState.NORMAL

        self._bg_rest = QColor()
        self._bg_hover = QColor()
        self._bg_pressed = QColor()
        self._bg_disabled = QColor()
        self._fg = QColor()
        self._border = QColor()
        self._border_accent = QColor()
        self._focus_color = QColor()

        self._radius = 4
        self._is_dark = False

        self._ripple = RippleEffect(self)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)

        self._theme_applied = False
        self._init_theme_aware()
        self._theme_applied = True

    # ── theme ──────────────────────────────────────────────

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._radius = r.int("component.button_radius")
        self._focus_color = r.color("semantic.focus_ring")
        self._is_dark = theme.is_dark

        control = getattr(theme.component, self.control_tokens_key, None)
        if control is not None:
            self._bg_rest = r.color(control.rest) if control.rest else QColor()
            self._bg_hover = r.color(control.hover) if control.hover else QColor()
            self._bg_pressed = r.color(control.pressed) if control.pressed else QColor()
            self._bg_disabled = r.color(control.disabled) if control.disabled else QColor()

        if self.fg_ref:
            self._fg = r.color(self.fg_ref)
        if self.border_ref:
            self._border = r.color(self.border_ref)
        if self.border_accent_ref:
            self._border_accent = r.color(self.border_accent_ref)

        self._bg_ani.stop()
        self._bg_obj.backgroundColor = self._bg_rest
        self.update()

    # ── state machine ──────────────────────────────────────

    def _set_state(self, state: _ButtonState) -> None:
        if self._state != state:
            self._state = state
            self._start_bg_animation()

            if state is _ButtonState.PRESSED:
                self._start_press_translate()
            else:
                self._start_release_translate()

    def _target_bg(self) -> QColor:
        if not self.isEnabled():
            return self._bg_disabled if self._bg_disabled.alpha() > 0 else self._bg_rest
        if self._state is _ButtonState.PRESSED:
            return self._bg_pressed
        if self._state is _ButtonState.HOVER:
            return self._bg_hover
        return self._bg_rest

    def enterEvent(self, e):
        self._set_state(_ButtonState.HOVER)
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._set_state(_ButtonState.NORMAL)
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._set_state(_ButtonState.PRESSED)
            self._ripple.start(e.position())
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._set_state(_ButtonState.NORMAL)
        super().mouseReleaseEvent(e)

    def changeEvent(self, e):
        if e.type() == e.Type.EnabledChange:
            self.update()
        super().changeEvent(e)

    # ── drawing ────────────────────────────────────────────

    def _draw_background(self, painter: QPainter) -> None:
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)

        from PyQt6.QtCore import QAbstractAnimation
        bg = self._animated_bg if self._bg_ani.state() == QAbstractAnimation.State.Running else self._target_bg()
        if bg.alpha() > 0:
            path = QPainterPath()
            path.addRoundedRect(rect, self._radius, self._radius)
            painter.fillPath(path, QBrush(bg))

        if self._border.alpha() > 0:
            path = QPainterPath()
            path.addRoundedRect(rect, self._radius, self._radius)

            is_flat = (not self.isEnabled()
                       or self._state is _ButtonState.PRESSED
                       or not self.border_accent_ref
                       or self._border_accent.alpha() == 0)
            if is_flat:
                pen = QPen(self._border, 1)
            else:
                # WinUI ControlElevationBorderBrush — 3px tall linear gradient
                # Dark: top→bottom (bright→subtle)
                # Light: bottom→top (bright→subtle)  via ScaleY="-1"
                if self._is_dark:
                    start = rect.topLeft()
                    end = rect.topLeft() + QPointF(0, 3)
                else:
                    start = rect.bottomLeft() - QPointF(0, 2)
                    end = rect.bottomLeft() + QPointF(0, 1)
                grad = QLinearGradient(start, end)
                grad.setColorAt(0.33, self._border_accent)
                grad.setColorAt(1.0, self._border)
                pen = QPen(QBrush(grad), 1)
            pen.setCosmetic(True)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)

    # ── paint ──────────────────────────────────────────────

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self.isEnabled():
            painter.setOpacity(_DISABLED_OPACITY)

        painter.save()
        if self._translate_y > 0:
            painter.translate(0, self._translate_y)
        self._draw_indicator(painter)
        painter.restore()

        self._ripple.paint(painter, QRectF(self.rect()), self._radius)

        if not self.isEnabled():
            painter.setOpacity(1.0)

        if self.hasFocus():
            FocusRing.paint(painter, QRectF(self.rect()), self._focus_color, self._radius)

    def _draw_indicator(self, painter: QPainter) -> None:
        raise NotImplementedError

    # ── size ───────────────────────────────────────────────

    def sizeHint(self):
        fm = QFontMetrics(self.font())
        tw = fm.horizontalAdvance(self.text().replace("&", ""))
        th = fm.height()
        w = tw + 24
        h = max(th, 16) + 8
        return QSize(max(w, 64), max(h, 32))
