"""Focus ring — rounded rectangle focus indicator matching Win11 style."""

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QPen


class FocusRing:
    """Paint helper for the Win11-style keyboard focus indicator."""

    @staticmethod
    def paint(painter: QPainter, rect: QRectF, color: QColor, radius: int = 4, width: int = 2) -> None:
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        pen = QPen(color, width)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        path = QPainterPath()
        r = rect.adjusted(width / 2, width / 2, -width / 2, -width / 2)
        path.addRoundedRect(r, radius, radius)
        painter.drawPath(path)
        painter.restore()
