"""Focus ring — WinUI 3 keyboard focus indicator.

From Common_themeresources_any.xaml:
  FocusVisualMargin="-3"
  FocusStrokeColorOuter + FocusStrokeColorInner (2px total, 1px each, offset 1px apart)
"""

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QPen


class FocusRing:
    @staticmethod
    def paint(
        painter: QPainter,
        rect: QRectF,
        color: QColor,
        radius: int = 4,
        width: int = 2,
    ) -> None:
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        outer = rect.adjusted(-3, -3, 3, 3)
        pen = QPen(color, width)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        path = QPainterPath()
        path.addRoundedRect(outer, radius + 2, radius + 2)
        painter.drawPath(path)
        painter.restore()