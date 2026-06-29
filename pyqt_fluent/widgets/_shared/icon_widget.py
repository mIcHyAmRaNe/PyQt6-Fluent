"""Theme-aware SVG icon widget."""

from __future__ import annotations

from PyQt6.QtCore import QByteArray, QFile, QRectF
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QWidget
from PyQt6.QtXml import QDomDocument

from ...tokens.theme import ThemeDefinition, ThemeManager
from .theme_aware import ThemeAwareWidget


class IconWidget(ThemeAwareWidget, QWidget):
    """SVG icon that auto-colours from a theme token."""

    def __init__(self, icon_path: str = "", color_ref: str = "semantic.control_fg",
                 fill_ref: str = "", parent=None):
        super().__init__(parent)
        self._color_ref = color_ref
        self._fill_ref = fill_ref
        self._color = QColor()
        self._fill = QColor()
        self._svg_data = QByteArray()
        if icon_path:
            self.load(icon_path)
        self._init_theme_aware()

    def load(self, path: str) -> None:
        f = QFile(path)
        if f.open(QFile.OpenModeFlag.ReadOnly):
            self._svg_data = f.readAll()
            f.close()
        self.update()

    def set_color_ref(self, ref: str) -> None:
        self._color_ref = ref
        self._apply_theme(ThemeManager.instance().theme())

    def set_fill_ref(self, ref: str) -> None:
        self._fill_ref = ref
        self._apply_theme(ThemeManager.instance().theme())

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._color = r.color(self._color_ref)
        if self._fill_ref:
            self._fill = r.color(self._fill_ref)
        self.update()

    def _svg_color(self, c: QColor) -> str:
        return f"rgba({c.red()},{c.green()},{c.blue()},{c.alphaF()})"

    def paintEvent(self, e) -> None:
        if self._svg_data.isEmpty():
            return
        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform
        )

        dom = QDomDocument()
        dom.setContent(self._svg_data)
        stroke_str = self._svg_color(self._color)

        path_nodes = dom.elementsByTagName("path")
        for i in range(path_nodes.length()):
            el = path_nodes.at(i).toElement()
            el.setAttribute("stroke", stroke_str)
            if self._fill_ref:
                el.setAttribute("fill", self._svg_color(self._fill))
            elif el.attribute("fill") in ("currentColor", ""):
                el.setAttribute("fill", stroke_str)

        if self._fill_ref:
            g_nodes = dom.elementsByTagName("g")
            for i in range(g_nodes.length()):
                el = g_nodes.at(i).toElement()
                el.setAttribute("fill", self._svg_color(self._fill))

        renderer = QSvgRenderer(dom.toByteArray())
        renderer.render(painter, QRectF(self.rect()))
        painter.end()
