"""Theme-aware SVG icon widget."""

from PyQt6.QtCore import QByteArray, QFile, QRectF
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QWidget
from PyQt6.QtXml import QDomDocument


class IconWidget(QWidget):
    """A widget that renders an SVG icon with a themeable colour.

    The colour is applied by replacing stroke/fill attributes in the SVG
    before rendering — same technique as SvgTitleBarButton.
    """

    def __init__(self, icon_path: str = "", parent=None):
        super().__init__(parent)
        self._icon_path = icon_path
        self._color = QColor(0, 0, 0)
        self._svg_data = QByteArray()
        if icon_path:
            self.load(icon_path)

    def load(self, path: str) -> None:
        f = QFile(path)
        if f.open(QFile.OpenModeFlag.ReadOnly):
            self._svg_data = f.readAll()
            f.close()

    def set_color(self, color: QColor) -> None:
        self._color = color
        self.update()

    def paintEvent(self, e) -> None:
        if self._svg_data.isEmpty():
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)

        dom = QDomDocument()  # type: ignore[attr-defined]
        dom.setContent(self._svg_data)
        color_name = self._color.name()
        path_nodes = dom.elementsByTagName("path")
        for i in range(path_nodes.length()):
            el = path_nodes.at(i).toElement()
            el.setAttribute("stroke", color_name)

        renderer = QSvgRenderer(dom.toByteArray())
        renderer.render(painter, QRectF(self.rect()))
        painter.end()
