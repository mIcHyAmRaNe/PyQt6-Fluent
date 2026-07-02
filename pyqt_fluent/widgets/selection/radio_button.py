"""Win11 RadioButton — 8-state ring indicator + dot."""

from __future__ import annotations

from PyQt6.QtCore import QRectF, QSize, Qt
from PyQt6.QtGui import QBrush, QColor, QFontMetrics, QPainter, QPen
from PyQt6.QtWidgets import QAbstractButton, QSizePolicy

from ...tokens.theme import ThemeDefinition
from .._shared.checkable import CheckableIndicator, _CheckState
from .._shared.theme_aware import ThemeAwareWidget

_RING_SIZE = 18
_LABEL_SPACING = 8


class RadioButton(CheckableIndicator, ThemeAwareWidget, QAbstractButton):
    """Win11 RadioButton — 8-state ring indicator, click restricted to ring.

    Parameters
    ----------
    text:
        Label text.
    parent:
        Qt parent.
    checked_color:
        Override the accent colour used for the checked state.
    """

    def __init__(self, text="", parent=None, checked_color=None):
        super().__init__(parent)
        self.setText(text)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self._init_checkable()
        self._label_spacing = _LABEL_SPACING

        if checked_color:
            self._light_checked = QColor(checked_color)
            self._dark_checked = QColor(checked_color)

        self.setStyleSheet("RadioButton { background: transparent; border: none; }")
        self._init_theme_aware()

    # ── geometry ────────────────────────────────────────────

    def _indicator_rect(self) -> QRectF:
        h = self.height()
        y = (h - _RING_SIZE) / 2
        return QRectF(4, y, _RING_SIZE, _RING_SIZE)

    def _checkmark_rect(self) -> QRectF:
        ring = self._indicator_rect()
        margin = 4.0
        return ring.adjusted(margin, margin, -margin, -margin)

    # ── theme ───────────────────────────────────────────────

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        self._resolve_theme_colors(theme)
        r = theme.resolver()
        self._border = r.color("gray.400") if not theme.is_dark else r.color("gray.500")
        self.update()

    # ── paint ───────────────────────────────────────────────

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        ring = self._indicator_rect()
        s = self._state()

        self._paint_scale(painter, ring.center())

        from ...tokens.theme import ThemeManager
        theme = ThemeManager.instance().theme()
        r = theme.resolver()

        border = self._border_color(s, theme)
        bg = self._bg_color(s, theme)

        # draw ring — state-dependent border width (WinUI 3 / FluUI spec)
        # unchecked: 1px, checked: 4px, checked+disabled: 3px
        opacity = 0.5 if s in (_CheckState.DISABLED, _CheckState.CHECKED_DISABLED) else 1.0
        painter.setOpacity(opacity)

        if bg.alpha() > 0:
            painter.setBrush(QBrush(bg))
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)

        if s in (_CheckState.CHECKED, _CheckState.CHECKED_HOVER, _CheckState.CHECKED_PRESSED):
            bw = 4.0 if s != _CheckState.CHECKED_HOVER else 3.0
        elif s == _CheckState.CHECKED_DISABLED:
            bw = 3.0
        else:
            bw = 1.0
        painter.setPen(QPen(border, bw))
        painter.drawEllipse(ring)

        # draw centre dot when checked
        if self.isChecked():
            dot = self._checkmark_rect()
            painter.setBrush(QBrush(QColor("#FFFFFF")))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(dot)

        painter.setOpacity(1.0)

        self._paint_scale_restore(painter)

        # label
        self._paint_label(painter, ring.right(), r, theme)

        # focus
        self._paint_focus(painter)

    def sizeHint(self):
        fm = QFontMetrics(self.font())
        tw = fm.horizontalAdvance(self.text().replace("&", ""))
        return QSize(int(4 + _RING_SIZE + _LABEL_SPACING + tw + 8),
                     max(fm.height(), _RING_SIZE) + 8)
