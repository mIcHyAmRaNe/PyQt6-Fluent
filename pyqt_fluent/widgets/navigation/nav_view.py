from __future__ import annotations

from PyQt6.QtCore import QRect, QRectF, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QMouseEvent, QPainter, QPainterPath
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

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
        self._compact = False

        self._custom_fg: QColor | None = None
        self._custom_selected_bg: QColor | None = None
        self._custom_selected_fg: QColor | None = None
        self._custom_hover: QColor | None = None
        self._custom_pressed: QColor | None = None
        self._custom_pill: QColor | None = None

        self._fg = QColor()
        self._selected_bg = QColor()
        self._selected_fg = QColor()
        self._hover_bg = QColor()
        self._pressed_bg = QColor()
        self._pill_accent = QColor()

        self.setFixedHeight(36)
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._init_theme_aware()

    def set_colors(self, fg=None, selected_bg=None, selected_fg=None, hover=None, pressed=None, pill_accent=None):
        self._custom_fg = QColor(fg) if fg else None
        self._custom_selected_bg = QColor(selected_bg) if selected_bg else None
        self._custom_selected_fg = QColor(selected_fg) if selected_fg else None
        self._custom_hover = QColor(hover) if hover else None
        self._custom_pressed = QColor(pressed) if pressed else None
        self._custom_pill = QColor(pill_accent) if pill_accent else None
        if fg:
            self._fg = QColor(fg)
        if selected_bg:
            self._selected_bg = QColor(selected_bg)
        if selected_fg:
            self._selected_fg = QColor(selected_fg)
        if hover:
            self._hover_bg = QColor(hover)
        if pressed:
            self._pressed_bg = QColor(pressed)
        if pill_accent:
            self._pill_accent = QColor(pill_accent)
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
        if not self._custom_fg:
            self._fg = r.color("component.nav_fg")
        if not self._custom_selected_bg:
            self._selected_bg = r.color("component.nav_selected_bg")
        if not self._custom_selected_fg:
            self._selected_fg = r.color("component.nav_selected_fg")
        if not self._custom_hover:
            self._hover_bg = r.color("component.nav_item_hover")
        if not self._custom_pressed:
            self._pressed_bg = r.color("component.nav_item_pressed")
        if not self._custom_pill:
            self._pill_accent = r.color("component.nav_pill_accent")
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
            if self.rect().contains(e.pos()):
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
            # WinUI 3 pill indicator — 3x16px vertical accent bar on left edge
            pill = QRectF(0, (rect.height() - 16) / 2.0, 3, 16)
            painter.setBrush(self._pill_accent)
            painter.setPen(Qt.PenStyle.NoPen)
            pill_path = QPainterPath()
            pill_path.addRoundedRect(pill, 1.5, 1.5)
            painter.fillPath(pill_path, self._pill_accent)
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

        label = self._icon_text or self._text[:2]
        if self._compact:
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, label)
        else:
            icon_w = 0
            if self._icon_text:
                icon_w = 24
                painter.drawText(
                    QRect(12, 0, icon_w, rect.height()),
                    Qt.AlignmentFlag.AlignCenter,
                    self._icon_text,
                )
            text_x = 12 + icon_w + 8
            text_rect = QRect(text_x, 0, rect.width() - text_x - 12, rect.height())
            painter.drawText(
                text_rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._text
            )

    def set_compact(self, compact: bool) -> None:
        self._compact = compact
        self.update()

    def sizeHint(self):
        return self.size()


class NavigationView(ThemeAwareWidget, QWidget):
    qss_role = "fluent_navview"

    current_changed = pyqtSignal(int)

    def __init__(
        self,
        parent=None,
        bg_color=None,
        fg_color=None,
        selected_bg=None,
        selected_fg=None,
        item_hover=None,
        item_pressed=None,
        nav_width=240,
    ):
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
        self._pill_accent = QColor()
        self._nav_items: list[NavItem] = []
        self._current_index = -1
        self._compact = False
        self._expanded_width = self._custom_nav_width
        self._collapsed_width = 48

        self.setFixedWidth(self._expanded_width)

        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        self._header_widget = QWidget()
        self._header_widget.setFixedHeight(48)
        self._header_layout = QHBoxLayout(self._header_widget)
        self._header_layout.setContentsMargins(8, 0, 8, 0)
        self._header_layout.setSpacing(0)

        self._toggle_btn = QPushButton("☰")
        self._toggle_btn.setFixedSize(32, 32)
        self._toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._toggle_btn.clicked.connect(self._toggle_collapse)
        self._header_layout.addWidget(self._toggle_btn)

        self._header_label = QLabel("Navigation")
        self._header_layout.addWidget(self._header_label, 1)
        self._layout.addWidget(self._header_widget)

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

    def _toggle_collapse(self) -> None:
        self._compact = not self._compact
        w = self._collapsed_width if self._compact else self._expanded_width
        self.setFixedWidth(w)
        self._header_label.setVisible(not self._compact)
        for item in self._nav_items:
            item.set_compact(self._compact)
        self.update()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        is_dark = theme.is_dark
        self._bg = self._custom_bg if self._custom_bg else r.color("component.nav_bg")
        self._fg = self._custom_fg if self._custom_fg else r.color("component.nav_fg")
        self._selected_bg = (
            self._custom_selected_bg
            if self._custom_selected_bg
            else r.color("component.nav_selected_bg")
        )
        self._selected_fg = (
            self._custom_selected_fg
            if self._custom_selected_fg
            else r.color("component.nav_selected_fg")
        )
        self._item_hover = (
            self._custom_item_hover
            if self._custom_item_hover
            else r.color("component.nav_item_hover")
        )
        self._item_pressed = (
            self._custom_item_pressed
            if self._custom_item_pressed
            else r.color("component.nav_item_pressed")
        )

        border = r.color("component.nav_border")

        # Use proper theme colors for toggle button
        btn_bg = r.color("palette.white_10") if is_dark else r.color("palette.black_8")
        btn_hover = r.color("palette.white_20") if is_dark else r.color("palette.black_10")
        btn_pressed = r.color("palette.white_20") if is_dark else r.color("palette.black_20")

        rh = 4  # radius for header
        self._header_label.setStyleSheet(f"""
QLabel {{
    color: {self._fg.name()};
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 16px;
    font-weight: 600;
    background: transparent;
    padding-left: 8px;
}}
""")
        self._toggle_btn.setStyleSheet(f"""
QPushButton {{
    color: {self._fg.name()};
    background-color: {btn_bg.name(QColor.NameFormat.HexArgb)};
    border: none;
    border-radius: {rh}px;
    font-size: 16px;
    font-weight: 600;
}}
QPushButton:hover {{
    background-color: {btn_hover.name(QColor.NameFormat.HexArgb)};
}}
QPushButton:pressed {{
    background-color: {btn_pressed.name(QColor.NameFormat.HexArgb)};
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

        self._pill_accent = r.color("component.nav_pill_accent")
        for item in self._nav_items:
            item.set_colors(
                fg=self._fg,
                selected_bg=self._selected_bg,
                selected_fg=self._selected_fg,
                hover=self._item_hover,
                pressed=self._item_pressed,
                pill_accent=self._pill_accent,
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
                pill_accent=self._pill_accent,
            )

        item.clicked.connect(self._on_item_clicked)
        self._nav_items.append(item)
        self._scroll_layout.takeAt(self._scroll_layout.count() - 1)
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
