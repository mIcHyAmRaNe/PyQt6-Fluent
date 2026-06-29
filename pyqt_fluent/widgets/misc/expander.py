from __future__ import annotations

from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QBrush, QPen, QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class Expander(ThemeAwareWidget, QWidget):
    expanded_changed = pyqtSignal(bool)

    def __init__(self, parent=None, title="", bg_color=None, fg_color=None,
                 header_hover=None, border_color=None, arrow_color=None):
        super().__init__(parent)
        self._title = title
        self._expanded = True
        self._header_height = 36
        self._hovered = False

        self._bg = QColor()
        self._fg = QColor()
        self._header_hover = QColor()
        self._border = QColor()
        self._arrow_color = QColor()

        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_header_hover = QColor(header_hover) if header_hover else None
        self._custom_border = QColor(border_color) if border_color else None
        self._custom_arrow = QColor(arrow_color) if arrow_color else None

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._content_widget = QWidget()
        self._content_layout = QVBoxLayout(self._content_widget)
        self._content_layout.setContentsMargins(8, 8, 8, 8)
        self._layout.addWidget(self._content_widget)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setMouseTracking(True)
        self._init_theme_aware()

    def set_title(self, text: str):
        self._title = text
        self.update()

    def set_content(self, widget: QWidget):
        self._content_layout.addWidget(widget)

    def set_expanded(self, expanded: bool):
        self._expanded = expanded
        self._content_widget.setVisible(expanded)
        self.expanded_changed.emit(expanded)
        self.update()

    def is_expanded(self) -> bool:
        return self._expanded

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._bg = self._custom_bg if self._custom_bg else r.color("component.expander_content_bg")
        self._fg = self._custom_fg if self._custom_fg else r.color("component.expander_header_bg")
        self._header_hover = self._custom_header_hover if self._custom_header_hover else r.color("component.expander_header_hover")
        self._border = self._custom_border if self._custom_border else r.color("component.expander_border")
        self._arrow_color = self._custom_arrow if self._custom_arrow else r.color("component.expander_arrow")
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        header_rect = QRectF(0, 0, w, self._header_height)

        header_bg = self._header_hover if self._hovered else self._bg
        painter.fillRect(header_rect, QBrush(header_bg))

        pen = QPen(self._border, 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(int(header_rect.bottomLeft().x()), int(header_rect.bottomLeft().y()),
                         int(header_rect.bottomRight().x()), int(header_rect.bottomRight().y()))

        arrow_size = 8
        arrow_x = 12
        arrow_y = self._header_height / 2
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self._arrow_color))

        path = QPainterPath()
        if self._expanded:
            path.moveTo(arrow_x - arrow_size / 2, arrow_y - arrow_size / 3)
            path.lineTo(arrow_x, arrow_y + arrow_size / 3)
            path.lineTo(arrow_x + arrow_size / 2, arrow_y - arrow_size / 3)
        else:
            path.moveTo(arrow_x - arrow_size / 3, arrow_y - arrow_size / 2)
            path.lineTo(arrow_x + arrow_size / 3, arrow_y)
            path.lineTo(arrow_x - arrow_size / 3, arrow_y + arrow_size / 2)
        painter.drawPath(path)

        font = QFont("Segoe UI Variable, Segoe UI, sans-serif")
        font.setPixelSize(14)
        painter.setFont(font)
        painter.setPen(self._fg)
        text_rect = QRectF(arrow_x + arrow_size + 8, 0, w - arrow_x - arrow_size - 16, self._header_height)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self._title)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton and e.position().y() <= self._header_height:
            self.set_expanded(not self._expanded)
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        old = self._hovered
        self._hovered = e.position().y() <= self._header_height
        if old != self._hovered:
            self.update()
        super().mouseMoveEvent(e)

    def leaveEvent(self, e):
        self._hovered = False
        self.update()
        super().leaveEvent(e)
