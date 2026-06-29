from __future__ import annotations

from PyQt6.QtCore import QRect, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QFontMetrics, QMouseEvent, QPainter, QPainterPath
from PyQt6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QScrollArea,
                             QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class NavItem(ThemeAwareWidget, QWidget):
    clicked = pyqtSignal(int)

    def __init__(self, text: str, icon: str | None = None, index: int = 0, parent=None):
        super().__init__(parent)
        self._text = text
        self._icon_text = icon
        self._index = index
        self._selected = False
        self._hovered = False
        self._pressed = False

        self._custom_fg: QColor | None = None
        self._custom_selected_bg: QColor | None = None
        self._custom_selected_fg: QColor | None = None
        self._custom_hover: QColor | None = None
        self._custom_pressed: QColor | None = None

        self._fg = QColor()
        self._selected_bg = QColor()
        self._selected_fg = QColor()
        self._hover_bg = QColor()
        self._pressed_bg = QColor()

        self.setFixedHeight(36)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def set_colors(self, fg=None, selected_bg=None, selected_fg=None,
                   hover=None, pressed=None):
        self._custom_fg = QColor(fg) if fg else None
        self._custom_selected_bg = QColor(selected_bg) if selected_bg else None
        self._custom_selected_fg = QColor(selected_fg) if selected_fg else None
        self._custom_hover = QColor(hover) if hover else None
        self._custom_pressed = QColor(pressed) if pressed else None
        self.update()

    def set_selected(self, selected: bool) -> None:
        if self._selected != selected:
            self._selected = selected
            self.update()

    @property
    def is_selected(self) -> bool:
        return self._selected

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._fg = self._custom_fg if self._custom_fg else r.color("component.nav_fg")
        self._selected_bg = self._custom_selected_bg if self._custom_selected_bg else r.color("component.nav_selected_bg")
        self._selected_fg = self._custom_selected_fg if self._custom_selected_fg else r.color("component.nav_selected_fg")
        self._hover_bg = self._custom_hover if self._custom_hover else r.color("component.nav_item_hover")
        self._pressed_bg = self._custom_pressed if self._custom_pressed else r.color("component.nav_item_pressed")
        self.update()

    def enterEvent(self, e):
        self._hovered = True
        self.update()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._hovered = False
        self._pressed = False
        self.update()
        super().leaveEvent(e)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            self._pressed = True
            self.update()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.MouseButton.LeftButton:
            self._pressed = False
            if self.rect().contains(e.pos().toPoint()):
                self.clicked.emit(self._index)
            self.update()
        super().mouseReleaseEvent(e)

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        margin = 4
        if self._selected:
            bg = self._selected_bg
            path = QPainterPath()
            path.addRoundedRect(QRectF(rect).adjusted(margin, 0, -margin, 0), 5, 5)
            painter.fillPath(path, bg)
            fg = self._selected_fg
        elif self._pressed:
            bg = self._pressed_bg
            if bg.alpha() > 0:
                path = QPainterPath()
                path.addRoundedRect(QRectF(rect).adjusted(margin, 0, -margin, 0), 5, 5)
                painter.fillPath(path, bg)
            fg = self._fg
        elif self._hovered:
            bg = self._hover_bg
            if bg.alpha() > 0:
                path = QPainterPath()
                path.addRoundedRect(QRectF(rect).adjusted(margin, 0, -margin, 0), 5, 5)
                painter.fillPath(path, bg)
            fg = self._fg
        else:
            fg = self._fg

        painter.setPen(fg)
        f = QFont()
        f.setPixelSize(14)
        painter.setFont(f)

        icon_w = 0
        if self._icon_text:
            icon_w = 24
            painter.drawText(QRect(12, 0, icon_w, rect.height()),
                             Qt.AlignmentFlag.AlignCenter, self._icon_text)

        text_x = 12 + icon_w + 8
        text_rect = QRect(text_x, 0, rect.width() - text_x - 12, rect.height())
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                         self._text)

    def sizeHint(self):
        return self.size()


class NavigationView(ThemeAwareWidget, QWidget):
    qss_role = "fluent_navview"

    current_changed = pyqtSignal(int)

    def __init__(self, parent=None,
                 bg_color=None, fg_color=None,
                 selected_bg=None, selected_fg=None,
                 item_hover=None, item_pressed=None,
                 nav_width=240):
        super().__init__(parent)
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_selected_bg = QColor(selected_bg) if selected_bg else None
        self._custom_selected_fg = QColor(selected_fg) if selected_fg else None
        self._custom_item_hover = QColor(item_hover) if item_hover else None
        self._custom_item_pressed = QColor(item_pressed) if item_pressed else None
        self._custom_nav_width = nav_width

        self._bg = QColor()
        self._fg = QColor()
        self._selected_bg = QColor()
        self._selected_fg = QColor()
        self._item_hover = QColor()
        self._item_pressed = QColor()
        self._nav_items: list[NavItem] = []
        self._current_index = -1

        self.setFixedWidth(self._custom_nav_width)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._header = QLabel("Navigation")
        self._header.setFixedHeight(48)
        self._header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._header)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._scroll_area.setFrameShape(QFrame.Shape.NoFrame)

        self._scroll_content = QWidget()
        self._scroll_layout = QVBoxLayout(self._scroll_content)
        self._scroll_layout.setContentsMargins(8, 4, 8, 4)
        self._scroll_layout.setSpacing(2)
        self._scroll_layout.addStretch()
        self._scroll_area.setWidget(self._scroll_content)

        self._layout.addWidget(self._scroll_area)

        self._footer_layout = QVBoxLayout()
        self._footer_layout.setContentsMargins(8, 4, 8, 8)
        self._layout.addLayout(self._footer_layout)

        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._bg = self._custom_bg if self._custom_bg else r.color("component.nav_bg")
        self._fg = self._custom_fg if self._custom_fg else r.color("component.nav_fg")
        self._selected_bg = self._custom_selected_bg if self._custom_selected_bg else r.color("component.nav_selected_bg")
        self._selected_fg = self._custom_selected_fg if self._custom_selected_fg else r.color("component.nav_selected_fg")
        self._item_hover = self._custom_item_hover if self._custom_item_hover else r.color("component.nav_item_hover")
        self._item_pressed = self._custom_item_pressed if self._custom_item_pressed else r.color("component.nav_item_pressed")

        border = r.color("component.nav_border")

        self._header.setStyleSheet(f"""
QLabel {{
    color: {self._fg.name()};
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 16px;
    font-weight: 600;
    background: transparent;
}}
""")

        self.setStyleSheet(f"""
NavigationView {{
    background-color: {self._bg.name(QColor.NameFormat.HexArgb)};
    border-right: 1px solid {border.name(QColor.NameFormat.HexArgb)};
}}
NavigationView QScrollArea {{
    background: transparent;
    border: none;
}}
NavigationView QScrollArea > QWidget > QWidget {{
    background: transparent;
}}
NavigationView QScrollBar:vertical {{
    background: transparent;
    width: 6px;
    margin: 0;
}}
NavigationView QScrollBar::handle:vertical {{
    background-color: {r.color("component.scrollbar_fg").name(QColor.NameFormat.HexArgb)};
    border-radius: 3px;
    min-height: 24px;
}}
NavigationView QScrollBar::add-line:vertical,
NavigationView QScrollBar::sub-line:vertical {{
    height: 0;
}}
""")

        for item in self._nav_items:
            item.set_colors(
                fg=self._fg,
                selected_bg=self._selected_bg,
                selected_fg=self._selected_fg,
                hover=self._item_hover,
                pressed=self._item_pressed,
            )

    def add_item(self, text: str, icon: str | None = None) -> NavItem:
        index = len(self._nav_items)
        item = NavItem(text, icon=icon, index=index, parent=self._scroll_content)

        if self._fg.isValid():
            item.set_colors(
                fg=self._fg,
                selected_bg=self._selected_bg,
                selected_fg=self._selected_fg,
                hover=self._item_hover,
                pressed=self._item_pressed,
            )

        item.clicked.connect(self._on_item_clicked)
        self._nav_items.append(item)
        stretch = self._scroll_layout.takeAt(self._scroll_layout.count() - 1)
        self._scroll_layout.addWidget(item)
        self._scroll_layout.addStretch()

        if self._current_index < 0:
            self.set_current_index(0)

        return item

    def add_footer_item(self, text: str, icon: str | None = None) -> NavItem:
        item = NavItem(text, icon=icon, index=-1, parent=self)
        item.clicked.connect(self._on_footer_clicked)
        self._footer_layout.addWidget(item)
        return item

    def set_current_index(self, index: int) -> None:
        if index == self._current_index:
            return
        if self._current_index >= 0 and self._current_index < len(self._nav_items):
            self._nav_items[self._current_index].set_selected(False)
        self._current_index = index
        if 0 <= index < len(self._nav_items):
            self._nav_items[index].set_selected(True)
        self.current_changed.emit(index)

    def current_index(self) -> int:
        return self._current_index

    def _on_item_clicked(self, index: int) -> None:
        self.set_current_index(index)

    def _on_footer_clicked(self, index: int) -> None:
        pass

    def paintEvent(self, e) -> None:
        super().paintEvent(e)
