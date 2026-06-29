"""Drop shadow — anti-aliased shadow rendered in paintEvent."""

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QPainter, QPainterPath


class DropShadow:
    """Soft drop shadow rendered as concentric filled rounds.

    Use in paintEvent when Qt's QGraphicsDropShadowEffect is too expensive
    or causes clipping issues.
    """

    @staticmethod
    def paint(painter: QPainter, rect: QRectF, color: QColor = QColor(0, 0, 0, 40),
              radius: int = 8, offset: tuple[int, int] = (0, 2), spread: int = 4) -> None:
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        x, y = offset
        for i in range(spread, 0, -1):
            alpha = int(color.alpha() * (1.0 - i / (spread + 1)))
            c = QColor(color.red(), color.green(), color.blue(), alpha)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(c)
            margin = spread - i + 1
            r = rect.adjusted(-margin + x, -margin + y, margin + x, margin + y)
            path = QPainterPath()
            path.addRoundedRect(r, radius, radius)
            painter.drawPath(path)
        painter.restore()
