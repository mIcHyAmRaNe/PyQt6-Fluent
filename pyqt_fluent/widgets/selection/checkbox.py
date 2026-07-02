"""Win11 CheckBox — 8-state indicator + standalone checkmark icon."""

from __future__ import annotations

from PyQt6.QtCore import QRectF, QSize, Qt
from PyQt6.QtGui import QBrush, QColor, QFontMetrics, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import QAbstractButton, QSizePolicy

from ...icons.engine import FluentIcon, IconEngine
from ...tokens.theme import ThemeDefinition
from .._shared.checkable import CheckableIndicator, _CheckState
from .._shared.theme_aware import ThemeAwareWidget

_BOX_SIZE = 18
_LABEL_SPACING = 8
_CORNER = 4.0


class CheckBox(CheckableIndicator, ThemeAwareWidget, QAbstractButton):
    """Win11 CheckBox — 8-state indicator, click restricted to the box.

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
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self._init_checkable()
        self._label_spacing = _LABEL_SPACING

        if checked_color:
            self._light_checked = QColor(checked_color)
            self._dark_checked = QColor(checked_color)

        self._icon_engine = IconEngine.instance()
        self.setStyleSheet("CheckBox { background: transparent; border: none; }")
        self._init_theme_aware()

    # ── geometry ────────────────────────────────────────────

    def _indicator_rect(self) -> QRectF:
        h = self.height()
        y = (h - _BOX_SIZE) / 2
        return QRectF(4, y, _BOX_SIZE, _BOX_SIZE)

    def _checkmark_rect(self) -> QRectF:
        box = self._indicator_rect()
        margin = 2.5
        return box.adjusted(margin, margin, -margin, -margin)

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

        box = self._indicator_rect()
        s = self._state()

        self._paint_scale(painter, box.center())

        from ...tokens.theme import ThemeManager
        theme = ThemeManager.instance().theme()
        r = theme.resolver()

        border = self._border_color(s, theme)
        bg = self._bg_color(s, theme)

        # draw box
        path = QPainterPath()
        path.addRoundedRect(box, _CORNER, _CORNER)
        if bg.alpha() > 0:
            painter.fillPath(path, QBrush(bg))

        opacity = 0.5 if s in (_CheckState.DISABLED, _CheckState.CHECKED_DISABLED) else 1.0
        painter.setOpacity(opacity)
        painter.setPen(QPen(border, 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)
        painter.setOpacity(1.0)

        # draw checkmark
        if self.isChecked():
            cm = self._checkmark_rect()
            self._icon_engine.render(
                painter, cm, FluentIcon.CHECKMARK,
                color=QColor(0, 0, 0, 0), fill_color=QColor("#FFFFFF"),
            )

        self._paint_scale_restore(painter)

        # label
        self._paint_label(painter, box.right(), r, theme)

        # focus
        self._paint_focus(painter)

    def sizeHint(self):
        fm = QFontMetrics(self.font())
        tw = fm.horizontalAdvance(self.text().replace("&", ""))
        return QSize(int(4 + _BOX_SIZE + _LABEL_SPACING + tw + 8), max(fm.height(), _BOX_SIZE) + 8)
