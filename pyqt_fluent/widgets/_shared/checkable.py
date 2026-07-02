"""CheckableIndicator — shared mixin for CheckBox and RadioButton.

Extracts the duplicated 8-state machine, scale animation, hover/press
tracking, theme resolution, and focus ring painting from both widgets.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from PyQt6.QtCore import QPointF, QPropertyAnimation, QRectF, QSize, Qt, pyqtProperty
from PyQt6.QtGui import QColor, QFontMetrics, QPainter

from ...utils.animation import winui_easing
from .._shared.focus_ring import FocusRing

if TYPE_CHECKING:
    from ...tokens.theme import ThemeDefinition


class _CheckState(Enum):
    """8-state machine shared by CheckBox and RadioButton."""
    NORMAL = 0
    HOVER = 1
    PRESSED = 2
    CHECKED = 3
    CHECKED_HOVER = 4
    CHECKED_PRESSED = 5
    DISABLED = 6
    CHECKED_DISABLED = 7


class CheckableIndicator:
    """Mixin providing 8-state machine, scale animation, and theme resolution.

    Subclasses must implement:
        - ``_indicator_rect() -> QRectF`` — the clickable indicator area
        - ``_draw_indicator(painter, state, theme)`` — paint the indicator
        - Call ``self._init_checkable()`` at the end of ``__init__``.
    """

    _label_spacing: int = 8

    def _init_checkable(self) -> None:
        self._hovered = False
        self._pressed = False
        self._focus_color = QColor()
        self._scale = 1.0

        self._scale_ani = QPropertyAnimation(self, b"indicator_scale", self)
        self._scale_ani.setDuration(167)
        self._scale_ani.setEasingCurve(winui_easing())

        # Theme-resolved colours
        self._accent = QColor()
        self._accent_hover = QColor()
        self._accent_pressed = QColor()
        self._border = QColor()
        self._hover_bg = QColor()
        self._pressed_bg = QColor()
        self._unchecked_bg = QColor()
        self._disabled_border = QColor()
        self._disabled_bg = QColor()

        # Per-theme overrides
        self._light_checked = QColor()
        self._dark_checked = QColor()
        self._light_text = QColor()
        self._dark_text = QColor()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    # ── scale animation property ────────────────────────────

    def _get_indicator_scale(self) -> float:
        return self._scale

    def _set_indicator_scale(self, v: float) -> None:
        self._scale = v
        self.update()

    indicator_scale = pyqtProperty(float, _get_indicator_scale, _set_indicator_scale)

    # ── public API ──────────────────────────────────────────

    def set_checked_color(self, light, dark):
        """Override the accent colour for the checked state."""
        self._light_checked = QColor(light)
        self._dark_checked = QColor(dark)
        self.update()

    def set_text_color(self, light, dark):
        """Override the label text colour."""
        self._light_text = QColor(light)
        self._dark_text = QColor(dark)
        self.update()

    # ── geometry ────────────────────────────────────────────

    def _indicator_rect(self) -> QRectF:
        raise NotImplementedError

    def _checkmark_rect(self) -> QRectF:
        raise NotImplementedError

    def hitButton(self, pos) -> bool:
        return self._indicator_rect().contains(QPointF(pos))

    # ── state machine ───────────────────────────────────────

    def _state(self) -> _CheckState:
        if not self.isEnabled():
            return _CheckState.CHECKED_DISABLED if self.isChecked() else _CheckState.DISABLED
        if self.isChecked():
            if self._pressed:
                return _CheckState.CHECKED_PRESSED
            if self._hovered:
                return _CheckState.CHECKED_HOVER
            return _CheckState.CHECKED
        else:
            if self._pressed:
                return _CheckState.PRESSED
            if self._hovered:
                return _CheckState.HOVER
            return _CheckState.NORMAL

    def _checked_color(self, theme: ThemeDefinition) -> QColor:
        if self._light_checked.isValid() and self._dark_checked.isValid():
            return self._dark_checked if theme.is_dark else self._light_checked
        if self._light_checked.isValid():
            return self._light_checked
        if self._dark_checked.isValid():
            return self._dark_checked
        return self._accent

    def _border_color(self, s: _CheckState, theme: ThemeDefinition) -> QColor:
        if s in (_CheckState.CHECKED, _CheckState.CHECKED_HOVER, _CheckState.CHECKED_PRESSED):
            return self._checked_color(theme)
        if s in (_CheckState.DISABLED, _CheckState.CHECKED_DISABLED):
            return self._disabled_border
        return self._border

    def _bg_color(self, s: _CheckState, theme: ThemeDefinition | None) -> QColor:
        if s in (_CheckState.CHECKED, _CheckState.CHECKED_HOVER, _CheckState.CHECKED_PRESSED):
            return self._checked_color(theme) if theme else self._accent
        if s == _CheckState.HOVER:
            return self._hover_bg
        if s == _CheckState.PRESSED:
            return self._pressed_bg
        if s in (_CheckState.NORMAL, _CheckState.DISABLED):
            return self._unchecked_bg
        if s == _CheckState.CHECKED_DISABLED:
            return self._disabled_bg
        return QColor()

    def _resolve_theme_colors(self, theme: ThemeDefinition) -> None:
        """Resolve standard colours from theme. Subclasses call this in on_theme_applied."""
        r = theme.resolver()
        self._accent = r.color("semantic.accent")
        self._accent_hover = r.color("semantic.accent_hover")
        self._accent_pressed = r.color("semantic.accent_pressed")
        self._hover_bg = r.color("semantic.hover")
        self._pressed_bg = r.color("semantic.pressed")
        self._unchecked_bg = r.color("gray.700") if theme.is_dark else r.color("gray.200")
        self._disabled_border = r.color("gray.500") if theme.is_dark else r.color("gray.400")
        self._disabled_bg = r.color("gray.700") if theme.is_dark else r.color("gray.200")
        self._focus_color = r.color("semantic.focus_ring")
        self._light_text = QColor()
        self._dark_text = QColor()

    def _text_color(self, r, theme: ThemeDefinition) -> QColor:
        if self._light_text.isValid() or self._dark_text.isValid():
            return self._dark_text if theme.is_dark else self._light_text
        return r.color("semantic.control_fg")

    # ── events ──────────────────────────────────────────────

    def enterEvent(self, e):
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._hovered = False
        self._pressed = False
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.update()
        super().leaveEvent(e)

    def mouseMoveEvent(self, e):
        over = self._indicator_rect().contains(e.position())
        self.setCursor(Qt.CursorShape.PointingHandCursor if over else Qt.CursorShape.ArrowCursor)
        if over != self._hovered:
            self._hovered = over
            self.update()
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton and self._indicator_rect().contains(e.position()):
            self._pressed = True
            self._scale_ani.stop()
            self._scale_ani.setStartValue(self._scale)
            self._scale_ani.setEndValue(0.85)
            self._scale_ani.start()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self._pressed = False
            self._scale_ani.stop()
            self._scale_ani.setStartValue(self._scale)
            self._scale_ani.setEndValue(1.0)
            self._scale_ani.start()
        super().mouseReleaseEvent(e)

    # ── size ────────────────────────────────────────────────

    def sizeHint(self):
        fm = QFontMetrics(self.font())
        tw = fm.horizontalAdvance(self.text().replace("&", ""))
        indicator_size = self._indicator_rect().width()
        return QSize(int(4 + indicator_size + self._label_spacing + tw + 8),
                     max(fm.height(), indicator_size) + 8)

    # ── paint helpers ───────────────────────────────────────

    def _paint_scale(self, painter: QPainter, center: QPointF) -> None:
        """Apply scale transform around center if scale < 1.0."""
        if self._scale < 1.0:
            painter.save()
            painter.translate(center)
            painter.scale(self._scale, self._scale)
            painter.translate(-center)

    def _paint_scale_restore(self, painter: QPainter) -> None:
        if self._scale < 1.0:
            painter.restore()

    def _paint_label(self, painter: QPainter, indicator_right: float, r, theme: ThemeDefinition) -> None:
        """Paint the text label to the right of the indicator."""
        txt_color = self._text_color(r, theme)
        painter.setPen(txt_color)
        lx = indicator_right + self._label_spacing
        text_rect = QRectF(lx, 0, self.width() - lx, self.height())
        align = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        painter.drawText(text_rect, align, self.text())

    def _paint_focus(self, painter: QPainter) -> None:
        if self.hasFocus():
            FocusRing.paint(painter, self._indicator_rect(), self._focus_color)

