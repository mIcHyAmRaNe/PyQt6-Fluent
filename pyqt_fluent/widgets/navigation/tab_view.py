from __future__ import annotations

from PyQt6.QtCore import QPoint, QRect, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QMouseEvent, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import QTabBar, QTabWidget, QWidget

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class TabBar(ThemeAwareWidget, QTabBar):
    qss_role = "fluent_tabbar"

    def __init__(self, parent=None,
                 bg_color=None, fg_color=None,
                 selected_bg=None, selected_fg=None,
                 tab_hover=None, close_hover=None):
        super().__init__(parent)
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_selected_bg = QColor(selected_bg) if selected_bg else None
        self._custom_selected_fg = QColor(selected_fg) if selected_fg else None
        self._custom_tab_hover = QColor(tab_hover) if tab_hover else None
        self._custom_close_hover = QColor(close_hover) if close_hover else None

        self._hover_index = -1
        self._close_hover_index = -1
        self._close_click_index = -1
        self._hover_bg = QColor()
        self._selected_bg = QColor()
        self._selected_fg = QColor()
        self._fg = QColor()
        self._bg = QColor()
        self._border = QColor()
        self._close_hover_bg = QColor()
        self._close_size = 16
        self._close_margin = 6
        self._tab_min_width = 80
        self._tab_height = 36

        self.setMouseTracking(True)
        self.setExpanding(False)
        self.setDrawBase(False)
        self.setFixedHeight(self._tab_height)

        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._bg = self._custom_bg if self._custom_bg else r.color("component.tab_bg")
        self._fg = self._custom_fg if self._custom_fg else r.color("component.tab_fg")
        self._selected_bg = self._custom_selected_bg if self._custom_selected_bg else r.color("component.tab_selected_bg")
        self._selected_fg = self._custom_selected_fg if self._custom_selected_fg else r.color("component.tab_selected_fg")
        self._hover_bg = self._custom_tab_hover if self._custom_tab_hover else r.color("component.tab_hover_bg")
        self._border = r.color("component.tab_border")
        self._close_hover_bg = self._custom_close_hover if self._custom_close_hover else r.color("component.tab_close_hover")
        self.update()

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        super().mouseMoveEvent(e)
        old_hover = self._hover_index
        self._hover_index = self.tabAt(e.pos())
        old_close = self._close_hover_index
        self._close_hover_index = -1
        tab = self._hover_index
        if tab >= 0:
            cr = self._close_button_rect(tab)
            if cr.contains(e.pos()):
                self._close_hover_index = tab
        if old_hover != self._hover_index or old_close != self._close_hover_index:
            self.update()

    def leaveEvent(self, e):
        super().leaveEvent(e)
        if self._hover_index >= 0 or self._close_hover_index >= 0:
            self._hover_index = -1
            self._close_hover_index = -1
            self.update()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        tab = self.tabAt(e.pos())
        if tab >= 0:
            cr = self._close_button_rect(tab)
            if cr.contains(e.pos()):
                self._close_click_index = tab
                return
        self._close_click_index = -1
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        tab = self.tabAt(e.pos())
        if tab >= 0 and tab == self._close_click_index:
            cr = self._close_button_rect(tab)
            if cr.contains(e.pos()):
                self.tabCloseRequested.emit(tab)
        self._close_click_index = -1
        super().mouseReleaseEvent(e)

    def _close_button_rect(self, index: int) -> QRect:
        tr = self.tabRect(index)
        x = tr.right() - self._close_margin - self._close_size
        y = tr.center().y() - self._close_size // 2
        return QRect(x, y, self._close_size, self._close_size)

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for i in range(self.count()):
            tr = self.tabRect(i)
            selected = i == self.currentIndex()
            hovered = i == self._hover_index
            close_hovered = i == self._close_hover_index

            bg_color = self._selected_bg if selected else (self._hover_bg if hovered else self._bg)
            if bg_color.alpha() > 0:
                path = QPainterPath()
                radius = 5.0
                path.moveTo(tr.left(), tr.bottom())
                path.lineTo(tr.left(), tr.top() + radius)
                path.arcTo(QRectF(tr.left(), tr.top(), radius * 2, radius * 2), 180, -90)
                path.lineTo(tr.right() - radius, tr.top())
                path.arcTo(QRectF(tr.right() - radius * 2, tr.top(), radius * 2, radius * 2), 90, -90)
                path.lineTo(tr.right(), tr.bottom())
                path.closeSubpath()
                painter.fillPath(path, bg_color)

            fg = self._selected_fg if selected else self._fg
            painter.setPen(fg)
            f = QFont()
            f.setPixelSize(13)
            painter.setFont(f)

            label_rect = tr.adjusted(10, 0, -(self._close_size + self._close_margin + 4), 0)
            painter.drawText(label_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                             self.tabText(i))

            if close_hovered:
                cr = self._close_button_rect(i)
                cpath = QPainterPath()
                cpath.addRoundedRect(QRectF(cr), 3, 3)
                painter.fillPath(cpath, self._close_hover_bg)

                painter.setPen(QPen(fg, 1.5))
                cx = cr.center().x()
                cy = cr.center().y()
                s = 4
                painter.drawLine(QPoint(cx - s, cy - s), QPoint(cx + s, cy + s))
                painter.drawLine(QPoint(cx + s, cy - s), QPoint(cx - s, cy + s))
            elif selected:
                cr = self._close_button_rect(i)
                painter.setPen(QPen(fg, 1.5))
                cx = cr.center().x()
                cy = cr.center().y()
                s = 4
                painter.drawLine(QPoint(cx - s, cy - s), QPoint(cx + s, cy + s))
                painter.drawLine(QPoint(cx + s, cy - s), QPoint(cx - s, cy + s))


class TabView(ThemeAwareWidget, QTabWidget):
    qss_role = "fluent_tabview"

    tabCloseRequested = pyqtSignal(int)

    def __init__(self, parent=None,
                 bg_color=None, fg_color=None,
                 selected_bg=None, selected_fg=None,
                 tab_hover=None, close_hover=None):
        super().__init__(parent)
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_selected_bg = QColor(selected_bg) if selected_bg else None
        self._custom_selected_fg = QColor(selected_fg) if selected_fg else None
        self._custom_tab_hover = QColor(tab_hover) if tab_hover else None
        self._custom_close_hover = QColor(close_hover) if close_hover else None

        self._bar = TabBar(self, bg_color=bg_color, fg_color=fg_color,
                           selected_bg=selected_bg, selected_fg=selected_fg,
                           tab_hover=tab_hover, close_hover=close_hover)
        self._bar.tabCloseRequested.connect(self.tabCloseRequested)
        self.setTabBar(self._bar)
        self.setDocumentMode(True)

        self._custom_bar_bg = QColor(bg_color) if bg_color else None

        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        bg = self._custom_bg if self._custom_bg else r.color("component.window_bg")
        bar_bg = self._custom_bar_bg if self._custom_bar_bg else r.color("component.tab_bar_bg")
        border = r.color("component.tab_border")

        self.setStyleSheet(f"""
TabView::pane {{
    background-color: {bg.name(QColor.NameFormat.HexArgb)};
    border: none;
    border-top: 1px solid {border.name(QColor.NameFormat.HexArgb)};
    top: -1px;
}}
""")

    def add_tab(self, widget: QWidget, title: str) -> int:
        return self.addTab(widget, title)

    def remove_tab(self, index: int) -> None:
        self.removeTab(index)
