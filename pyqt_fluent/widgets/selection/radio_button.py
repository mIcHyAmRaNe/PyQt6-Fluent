"""Win11 RadioButton — 8-state ring indicator + dot."""

from __future__ import annotations

from enum import Enum
from importlib.resources import files as _resources

from PyQt6.QtCore import (QByteArray, QEasingCurve, QFile, QPointF,
                           QPropertyAnimation, QRectF, QSize, Qt, pyqtProperty)
from PyQt6.QtGui import QBrush, QColor, QFontMetrics, QPainter, QPen
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QAbstractButton, QSizePolicy
from PyQt6.QtXml import QDomDocument

from ...tokens.theme import ThemeDefinition
from .._shared.focus_ring import FocusRing
from .._shared.theme_aware import ThemeAwareWidget

_RING_SIZE = 16
_LABEL_SPACING = 8

# ── state machine ───────────────────────────────────────────


class RadioState(Enum):
    NORMAL = 0
    HOVER = 1
    PRESSED = 2
    CHECKED = 3
    CHECKED_HOVER = 4
    CHECKED_PRESSED = 5
    DISABLED = 6
    CHECKED_DISABLED = 7


def _load_svg(name: str) -> QByteArray:
    p = _resources("pyqt_fluent.resources").joinpath("icons", name)
    f = QFile(str(p))
    if f.open(QFile.OpenModeFlag.ReadOnly):
        d = f.readAll()
        f.close()
        return d
    return QByteArray()


def _svg_color(c: QColor) -> str:
    return f"rgba({c.red()},{c.green()},{c.blue()},{c.alphaF()})"


def _render_svg(painter: QPainter, data: QByteArray, rect: QRectF,
                stroke: QColor, fill: QColor | None = None) -> None:
    dom = QDomDocument()
    dom.setContent(data)
    sn = _svg_color(stroke)
    path_nodes = dom.elementsByTagName("path")
    for i in range(path_nodes.length()):
        el = path_nodes.at(i).toElement()
        el.setAttribute("stroke", sn)
        if fill is not None and el.attribute("fill") in ("currentColor", ""):
            el.setAttribute("fill", _svg_color(fill))
    renderer = QSvgRenderer(dom.toByteArray())
    renderer.render(painter, rect)


# ── widget ──────────────────────────────────────────────────


class RadioButton(ThemeAwareWidget, QAbstractButton):
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

        self._hovered = False
        self._pressed = False
        self._focus_color = QColor()
        self._scale = 1.0
        self._scale_ani = QPropertyAnimation(self, b"ring_scale", self)
        self._scale_ani.setDuration(83)
        e = QEasingCurve(QEasingCurve.Type.BezierSpline)
        e.addCubicBezierSegment(QPointF(0.1, 0.9), QPointF(0.2, 1.0), QPointF(1.0, 1.0))
        self._scale_ani.setEasingCurve(e)

        # checked colour override (per-theme)
        self._light_checked = QColor()
        self._dark_checked = QColor()
        if checked_color:
            self._light_checked = QColor(checked_color)
            self._dark_checked = QColor(checked_color)

        # state colours resolved from theme
        self._accent = QColor()
        self._accent_hover = QColor()
        self._accent_pressed = QColor()
        self._border = QColor()
        self._hover_bg = QColor()
        self._pressed_bg = QColor()
        self._disabled_border = QColor()
        self._disabled_bg = QColor()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("RadioButton { background: transparent; border: none; }")
        self._init_theme_aware()

    # ── press animation ──────────────────────────────────────

    def _get_ring_scale(self) -> float:
        return self._scale

    def _set_ring_scale(self, v: float) -> None:
        self._scale = v
        self.update()

    ring_scale = pyqtProperty(float, _get_ring_scale, _set_ring_scale)

    # ── public API ──────────────────────────────────────────

    def set_checked_color(self, light, dark):
        """Override the accent colour used for the checked state.

        Parameters
        ----------
        light, dark : str | QColor
            Colour in light / dark theme mode.
        """
        self._light_checked = QColor(light)
        self._dark_checked = QColor(dark)
        self.update()

    def set_text_color(self, light, dark):
        """Override the label text colour.

        Parameters
        ----------
        light, dark : str | QColor
            Colour in light / dark theme mode.
        """
        self._light_text = QColor(light)
        self._dark_text = QColor(dark)
        self.update()

    # ── geometry ────────────────────────────────────────────

    def _ring_rect(self) -> QRectF:
        h = self.height()
        y = (h - _RING_SIZE) / 2
        return QRectF(4, y, _RING_SIZE, _RING_SIZE)

    def _dot_rect(self) -> QRectF:
        ring = self._ring_rect()
        margin = 4.0
        return ring.adjusted(margin, margin, -margin, -margin)

    def hitButton(self, pos) -> bool:
        return self._ring_rect().contains(QPointF(pos))

    # ── state machine ───────────────────────────────────────

    def _state(self) -> RadioState:
        if not self.isEnabled():
            return RadioState.CHECKED_DISABLED if self.isChecked() else RadioState.DISABLED
        if self.isChecked():
            if self._pressed:
                return RadioState.CHECKED_PRESSED
            if self._hovered:
                return RadioState.CHECKED_HOVER
            return RadioState.CHECKED
        else:
            if self._pressed:
                return RadioState.PRESSED
            if self._hovered:
                return RadioState.HOVER
            return RadioState.NORMAL

    def _checked_color(self, theme: ThemeDefinition) -> QColor:
        if self._light_checked.isValid() and self._dark_checked.isValid():
            return self._dark_checked if theme.is_dark else self._light_checked
        if self._light_checked.isValid():
            return self._light_checked
        if self._dark_checked.isValid():
            return self._dark_checked
        return self._accent

    def _border_color(self, s: RadioState, theme: ThemeDefinition) -> QColor:
        if s in (RadioState.CHECKED, RadioState.CHECKED_HOVER, RadioState.CHECKED_PRESSED):
            return self._checked_color(theme)
        if s in (RadioState.DISABLED, RadioState.CHECKED_DISABLED):
            return self._disabled_border
        if s == RadioState.HOVER:
            return self._border
        return self._border  # NORMAL, PRESSED

    def _bg_color(self, s: RadioState, theme: ThemeDefinition | None) -> QColor:
        if s in (RadioState.CHECKED, RadioState.CHECKED_HOVER, RadioState.CHECKED_PRESSED):
            return self._checked_color(theme) if theme else self._accent
        if s == RadioState.HOVER:
            return self._hover_bg
        if s == RadioState.CHECKED_DISABLED:
            return self._disabled_bg
        return QColor()  # transparent (NORMAL, PRESSED, DISABLED)

    # ── theme ───────────────────────────────────────────────

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._accent = r.color("semantic.accent")
        self._accent_hover = r.color("semantic.accent_hover")
        self._accent_pressed = r.color("semantic.accent_pressed")
        self._border = r.color("semantic.control_border")
        self._hover_bg = r.color("semantic.hover")
        self._pressed_bg = r.color("semantic.pressed")
        self._disabled_border = r.color("gray.500") if theme.is_dark else r.color("gray.400")
        self._disabled_bg = r.color("gray.700") if theme.is_dark else r.color("gray.200")
        self._focus_color = r.color("semantic.focus_ring")
        self._light_text = QColor()
        self._dark_text = QColor()
        self.update()

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
        over = self._ring_rect().contains(e.position())
        self.setCursor(Qt.CursorShape.PointingHandCursor if over else Qt.CursorShape.ArrowCursor)
        if over != self._hovered:
            self._hovered = over
            self.update()
        super().mouseMoveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton and self._ring_rect().contains(e.position()):
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

    # ── paint ───────────────────────────────────────────────

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        ring = self._ring_rect()
        s = self._state()

        if self._scale < 1.0:
            painter.save()
            centre = ring.center()
            painter.translate(centre)
            painter.scale(self._scale, self._scale)
            painter.translate(-centre)

        from ...tokens.theme import ThemeManager
        tm = ThemeManager.instance()
        theme = tm.theme()
        r = theme.resolver()

        border = self._border_color(s, theme)
        bg = self._bg_color(s, theme)

        # ── draw ring ───────────────────────────────────────
        opacity = 0.5 if s in (RadioState.DISABLED, RadioState.CHECKED_DISABLED) else 1.0
        painter.setOpacity(opacity)

        if bg.alpha() > 0:
            painter.setBrush(QBrush(bg))
        else:
            painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(border, 1.5))
        painter.drawEllipse(ring)

        # ── draw centre dot when checked ────────────────────
        if self.isChecked():
            dot = self._dot_rect()
            painter.setBrush(QBrush(QColor("#FFFFFF")))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(dot)

        painter.setOpacity(1.0)

        if self._scale < 1.0:
            painter.restore()

        # ── label ───────────────────────────────────────────
        txt_color = self._text_color(r, theme)
        painter.setPen(txt_color)
        lx = ring.right() + _LABEL_SPACING
        r_ = QRectF(lx, 0, self.width() - lx, self.height())
        align = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        painter.drawText(r_, align, self.text())

        # ── focus ──────────────────────────────────────────
        if self.hasFocus():
            FocusRing.paint(painter, self._ring_rect(), self._focus_color)

    def _text_color(self, r, theme: ThemeDefinition) -> QColor:
        if self._light_text.isValid() or self._dark_text.isValid():
            return self._dark_text if theme.is_dark else self._light_text
        return r.color("semantic.control_fg")

    # ── size ────────────────────────────────────────────────

    def sizeHint(self):
        fm = QFontMetrics(self.font())
        tw = fm.horizontalAdvance(self.text().replace("&", ""))
        return QSize(int(4 + _RING_SIZE + _LABEL_SPACING + tw + 8),
                     max(fm.height(), _RING_SIZE) + 8)
