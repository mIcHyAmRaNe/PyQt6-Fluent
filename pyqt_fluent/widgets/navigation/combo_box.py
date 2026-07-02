from __future__ import annotations

from PyQt6.QtCore import QRectF, QSize, Qt
from PyQt6.QtGui import QBrush, QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import (
    QComboBox,
    QGraphicsDropShadowEffect,
    QListView,
    QSizePolicy,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
)

from ...icons.engine import IconEngine
from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget


class _ComboBoxDelegate(QStyledItemDelegate):
    """Custom delegate with left accent border for selected items."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._accent = QColor()
        self._hover_bg = QColor()
        self._selected_bg = QColor()
        self._selected_fg = QColor()
        self._fg = QColor()

    def set_colors(self, accent, hover_bg, selected_bg, selected_fg, fg):
        self._accent = accent
        self._hover_bg = hover_bg
        self._selected_bg = selected_bg
        self._selected_fg = selected_fg
        self._fg = fg

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index):
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = QRectF(option.rect)
        is_selected = bool(option.state & QStyle.StateFlag.State_Selected)
        is_hovered = bool(option.state & QStyle.StateFlag.State_MouseOver)

        # Background
        if is_selected:
            painter.fillRect(rect, QBrush(self._selected_bg))
        elif is_hovered:
            painter.fillRect(rect, QBrush(self._hover_bg))

        # Left accent bar (3px wide, 18px tall, centered) for selected
        if is_selected:
            bar_w = 3
            bar_h = 18
            bar_rect = QRectF(
                rect.x() + 1,
                rect.y() + (rect.height() - bar_h) / 2,
                bar_w,
                bar_h,
            )
            bar_path = QPainterPath()
            bar_path.addRoundedRect(bar_rect, 1.5, 1.5)
            painter.fillPath(bar_path, QBrush(self._accent))

        # Text
        text_rect = QRectF(rect.x() + 12, rect.y(), rect.width() - 12, rect.height())
        text = index.data(Qt.ItemDataRole.DisplayRole) or ""
        color = self._selected_fg if is_selected else self._fg
        painter.setPen(color)
        font = option.font
        if font.pointSize() <= 0:
            font.setPixelSize(14)
        painter.setFont(font)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)

        painter.restore()

    def sizeHint(self, option, index):
        return QSize(option.rect.width(), 36)


class ComboBox(ThemeAwareWidget, QComboBox):
    qss_role = "fluent_combo"

    def __init__(self, parent=None,
                 bg_color=None, fg_color=None, border_color=None,
                 dropdown_bg=None, item_hover=None):
        super().__init__(parent)
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_border = QColor(border_color) if border_color else None
        self._custom_dropdown_bg = QColor(dropdown_bg) if dropdown_bg else None
        self._custom_item_hover = QColor(item_hover) if item_hover else None

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(32)

        self._delegate = _ComboBoxDelegate(self)
        self.setItemDelegate(self._delegate)

        self.setView(QListView())
        self.view().setObjectName("fluent_combo_popup")
        self.view().setItemDelegate(self._delegate)

        self._icon_engine = IconEngine.instance()
        self._init_theme_aware()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        bg = self._custom_bg if self._custom_bg else r.color("component.combobox_bg")
        fg = self._custom_fg if self._custom_fg else r.color("component.combobox_fg")
        border = self._custom_border if self._custom_border else r.color("component.combobox_border")
        focus_border = r.color("component.combobox_focus_border")
        popup_bg = self._custom_dropdown_bg if self._custom_dropdown_bg else r.color("palette.combobox_popup_bg")
        popup_border = r.color("palette.combobox_popup_border")
        item_hover = self._custom_item_hover if self._custom_item_hover else r.color("component.combobox_item_hover")
        item_selected = r.color("component.combobox_item_selected")
        item_selected_fg = r.color("component.combobox_item_selected_fg")
        arrow = r.color("component.combobox_arrow")
        accent = r.color("semantic.accent")
        radius = r.int("component.control_radius")

        self._delegate.set_colors(accent, item_hover, item_selected, item_selected_fg, fg)

        self.setStyleSheet(f"""
ComboBox {{
    background-color: {bg.name(QColor.NameFormat.HexArgb)};
    color: {fg.name()};
    border: 1px solid {border.name(QColor.NameFormat.HexArgb)};
    border-radius: {radius}px;
    padding: 0 28px 0 8px;
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 14px;
}}
ComboBox:focus {{
    border: 2px solid {focus_border.name()};
    padding: 0 27px 0 7px;
}}
ComboBox:disabled {{
    opacity: 0.4;
}}
ComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border: none;
    border-top-right-radius: {radius}px;
    border-bottom-right-radius: {radius}px;
}}
ComboBox::down-arrow {{
    image: none;
    width: 8px;
    height: 8px;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {arrow.name()};
}}
ComboBox QAbstractItemView {{
    background-color: {popup_bg.name(QColor.NameFormat.HexArgb)};
    color: {fg.name()};
    border: 1px solid {popup_border.name(QColor.NameFormat.HexArgb)};
    border-radius: 5px;
    padding: 4px 0;
    outline: none;
    font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
    font-size: 14px;
    selection-background-color: transparent;
}}
ComboBox QAbstractItemView::item {{
    padding: 0 12px;
    min-height: 32px;
    margin: 2px 4px;
    border-radius: 4px;
}}
""")

        # Add shadow to popup view
        shadow = QGraphicsDropShadowEffect(self.view())
        shadow.setBlurRadius(16)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 51))
        self.view().setGraphicsEffect(shadow)
