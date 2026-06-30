from __future__ import annotations

from PyQt6.QtCore import QDate, QRectF, Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QFont, QMouseEvent, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget

_DAYS_LABELS = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
_CELL_SIZE = 28
_HEADER_H = 36
_PAD = 8


class _GridWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)
        self._hover_col = self._hover_row = -1
        self._clicked_col = self._clicked_row = -1

    def paintEvent(self, e):
        popup: _CalendarPopup = self.parent()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        start_x = (w - 7 * _CELL_SIZE) // 2

        first = popup._calendar_first_day()
        days_in_month = popup._calendar_days()
        today = QDate.currentDate()

        for row in range(6):
            for col in range(7):
                day_num = row * 7 + col - first + 1
                if day_num < 1 or day_num > days_in_month:
                    continue

                x = start_x + col * _CELL_SIZE
                y = row * _CELL_SIZE
                cell = QRectF(x, y, _CELL_SIZE, _CELL_SIZE)

                date_cell = QDate(popup._current_date.year(),
                                  popup._current_date.month(), day_num)
                is_today = date_cell == today
                is_selected = date_cell == popup._selected_date
                is_hover = (col == self._hover_col and row == self._hover_row)

                if is_selected:
                    painter.setBrush(QBrush(popup._day_selected_bg))
                    painter.setPen(Qt.PenStyle.NoPen)
                    path = QPainterPath()
                    path.addRoundedRect(cell.adjusted(2, 2, -2, -2), 4, 4)
                    painter.drawPath(path)
                elif is_hover:
                    painter.setBrush(QBrush(popup._day_hover))
                    painter.setPen(Qt.PenStyle.NoPen)
                    path = QPainterPath()
                    path.addRoundedRect(cell.adjusted(2, 2, -2, -2), 4, 4)
                    painter.drawPath(path)

                if is_today:
                    painter.setBrush(Qt.BrushStyle.NoBrush)
                    painter.setPen(QPen(popup._today_border, 1.5))
                    path = QPainterPath()
                    path.addRoundedRect(cell.adjusted(3, 3, -3, -3), 4, 4)
                    painter.drawPath(path)

                fg = popup._day_selected_fg if is_selected else popup._fg
                painter.setPen(fg)
                f = QFont()
                f.setPixelSize(12)
                painter.setFont(f)
                painter.drawText(cell, Qt.AlignmentFlag.AlignCenter, str(day_num))

    def mouseMoveEvent(self, e: QMouseEvent):
        pos = e.position()
        w = self.width()
        start_x = (w - 7 * _CELL_SIZE) // 2
        col = int((pos.x() - start_x) // _CELL_SIZE)
        row = int(pos.y() // _CELL_SIZE)
        self._hover_col = col if 0 <= col < 7 else -1
        self._hover_row = row if 0 <= row < 6 else -1
        self.update()

    def leaveEvent(self, e):
        self._hover_col = self._hover_row = -1
        self.update()
        super().leaveEvent(e)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.MouseButton.LeftButton:
            pos = e.position()
            w = self.width()
            start_x = (w - 7 * _CELL_SIZE) // 2
            col = int((pos.x() - start_x) // _CELL_SIZE)
            row = int(pos.y() // _CELL_SIZE)
            first = self.parent()._calendar_first_day()
            days_in_month = self.parent()._calendar_days()
            day_num = row * 7 + col - first + 1
            if 1 <= day_num <= days_in_month:
                date = QDate(self.parent()._current_date.year(),
                             self.parent()._current_date.month(), day_num)
                self.parent()._selected_date = date
                self.parent().date_selected.emit(date)
                self.update()


class _CalendarPopup(ThemeAwareWidget, QFrame):
    date_selected = pyqtSignal(QDate)

    def __init__(self, parent=None,
                 popup_bg=None, header_bg=None, header_fg=None,
                 day_hover=None, day_selected_bg=None, day_selected_fg=None,
                 today_border=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._current_date = QDate.currentDate()
        self._selected_date = QDate.currentDate()

        self._custom_popup_bg = QColor(popup_bg) if popup_bg else None
        self._custom_header_bg = QColor(header_bg) if header_bg else None
        self._custom_header_fg = QColor(header_fg) if header_fg else None
        self._custom_day_hover = QColor(day_hover) if day_hover else None
        self._custom_day_selected_bg = QColor(day_selected_bg) if day_selected_bg else None
        self._custom_day_selected_fg = QColor(day_selected_fg) if day_selected_fg else None
        self._custom_today_border = QColor(today_border) if today_border else None

        self._popup_bg = QColor()
        self._header_bg = QColor()
        self._header_fg = QColor()
        self._fg = QColor()
        self._day_hover = QColor()
        self._day_selected_bg = QColor()
        self._day_selected_fg = QColor()
        self._today_border = QColor()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(_HEADER_H)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(_PAD, 0, _PAD, 0)

        self._prev_btn = QPushButton("<")
        self._prev_btn.setFixedSize(28, 28)
        self._prev_btn.setFlat(True)
        self._prev_btn.clicked.connect(self._prev_month)

        self._month_label = QLabel()
        self._month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._next_btn = QPushButton(">")
        self._next_btn.setFixedSize(28, 28)
        self._next_btn.setFlat(True)
        self._next_btn.clicked.connect(self._next_month)

        hl.addWidget(self._prev_btn)
        hl.addWidget(self._month_label, 1)
        hl.addWidget(self._next_btn)

        self._header_widget = header
        layout.addWidget(header)

        day_labels = QWidget()
        day_labels.setFixedHeight(20)
        dl = QHBoxLayout(day_labels)
        dl.setContentsMargins(0, 0, 0, 0)
        dl.setSpacing(0)
        for label in _DAYS_LABELS:
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setFixedWidth(_CELL_SIZE)
            dl.addWidget(lbl)
        layout.addWidget(day_labels)

        self._grid = _GridWidget(self)
        self._grid.setFixedSize(7 * _CELL_SIZE, 6 * _CELL_SIZE)
        g_layout = QHBoxLayout()
        g_layout.setContentsMargins(0, 0, 0, _PAD)
        g_layout.addStretch()
        g_layout.addWidget(self._grid)
        g_layout.addStretch()
        layout.addLayout(g_layout)

        self._update_month_label()
        self._init_theme_aware()

    def _calendar_first_day(self) -> int:
        first = QDate(self._current_date.year(), self._current_date.month(), 1)
        return (first.dayOfWeek() - 1) % 7

    def _calendar_days(self) -> int:
        return self._current_date.daysInMonth()

    def _prev_month(self):
        self._current_date = self._current_date.addMonths(-1)
        self._update_month_label()
        self._grid.update()

    def _next_month(self):
        self._current_date = self._current_date.addMonths(1)
        self._update_month_label()
        self._grid.update()

    def _update_month_label(self):
        self._month_label.setText(self._current_date.toString("MMMM yyyy"))

    def selected_date(self):
        return self._selected_date

    def set_selected_date(self, d: QDate):
        self._selected_date = d
        if d.month() != self._current_date.month() or d.year() != self._current_date.year():
            self._current_date = QDate(d.year(), d.month(), 1)
            self._update_month_label()
        self._grid.update()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        c = theme.component
        self._popup_bg = self._custom_popup_bg if self._custom_popup_bg else r.color(c.picker_popup_bg)
        self._header_bg = self._custom_header_bg if self._custom_header_bg else r.color(c.picker_header_bg)
        self._header_fg = self._custom_header_fg if self._custom_header_fg else r.color(c.picker_header_fg)
        self._fg = r.color(c.picker_fg)
        self._day_hover = self._custom_day_hover if self._custom_day_hover else r.color(c.picker_day_hover)
        self._day_selected_bg = self._custom_day_selected_bg if self._custom_day_selected_bg else r.color(c.picker_day_selected_bg)
        self._day_selected_fg = self._custom_day_selected_fg if self._custom_day_selected_fg else r.color(c.picker_day_selected_fg)
        self._today_border = self._custom_today_border if self._custom_today_border else r.color(c.picker_day_today_border)
        self._header_widget.setStyleSheet(f"""
QWidget {{
    background: {self._header_bg.name(QColor.NameFormat.HexArgb)};
    color: {self._header_fg.name()};
}}
QPushButton {{
    background: transparent;
    color: {self._header_fg.name()};
    border: none;
    font-weight: bold;
    font-size: 14px;
}}
QPushButton:hover {{
    background: rgba(255,255,255,0.15);
    border-radius: 4px;
}}
""")
        fg_name = self._fg.name()
        self._set_days_style(fg_name)

    def _set_days_style(self, fg: str):
        for child in self.findChildren(QLabel):
            if child.text() in _DAYS_LABELS:
                child.setStyleSheet(f"color: {fg}; background: transparent; font-size: 11px;")

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 8, 8)
        painter.fillPath(path, QBrush(self._popup_bg))

    def showEvent(self, e):
        super().showEvent(e)
        w = max(self._grid.width() + 2 * _PAD, self._header_widget.width())
        self.setFixedSize(w, _HEADER_H + 20 + 6 * _CELL_SIZE + _PAD)


class DatePicker(ThemeAwareWidget, QWidget):
    date_changed = pyqtSignal(QDate)

    def __init__(self, parent=None,
                 bg_color=None, fg_color=None, border_color=None,
                 popup_bg=None, header_bg=None, header_fg=None,
                 day_hover=None, day_selected_bg=None, day_selected_fg=None):
        super().__init__(parent)
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_fg = QColor(fg_color) if fg_color else None
        self._custom_border = QColor(border_color) if border_color else None

        self._bg = QColor()
        self._fg = QColor()
        self._border = QColor()

        self._date = QDate.currentDate()

        self.setFixedHeight(32)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 0, 4, 0)

        self._label = QLabel(self._date.toString("yyyy-MM-dd"))
        self._label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self._label, 1)

        self._arrow = QPushButton("▼")
        self._arrow.setFixedSize(24, 24)
        self._arrow.setFlat(True)
        self._arrow.clicked.connect(self._toggle_popup)
        layout.addWidget(self._arrow)

        self._popup = _CalendarPopup(
            self, popup_bg=popup_bg, header_bg=header_bg, header_fg=header_fg,
            day_hover=day_hover, day_selected_bg=day_selected_bg,
            day_selected_fg=day_selected_fg,
            today_border=border_color,
        )
        self._popup.date_selected.connect(self._on_date_selected)

        self._init_theme_aware()

    def date(self) -> QDate:
        return self._date

    def set_date(self, d: QDate):
        self._date = d
        self._label.setText(d.toString("yyyy-MM-dd"))
        self._popup.set_selected_date(d)
        self.date_changed.emit(d)
        self.update()

    def _toggle_popup(self):
        if self._popup.isVisible():
            self._popup.hide()
        else:
            pos = self.mapToGlobal(self.rect().bottomLeft())
            self._popup.move(pos)
            self._popup.set_selected_date(self._date)
            self._popup.show()

    def _on_date_selected(self, d: QDate):
        self.set_date(d)
        self._popup.hide()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        c = theme.component
        self._bg = self._custom_bg if self._custom_bg else r.color(c.picker_bg)
        self._fg = self._custom_fg if self._custom_fg else r.color(c.picker_fg)
        self._border = self._custom_border if self._custom_border else r.color(c.picker_border)
        radius = r.int("component.control_radius")
        bg = self._bg.name(QColor.NameFormat.HexArgb)
        fg = self._fg.name()
        border = self._border.name(QColor.NameFormat.HexArgb)
        self.setStyleSheet(f"""
DatePicker {{
    background-color: {bg};
    border: 1px solid {border};
    border-radius: {radius}px;
}}
DatePicker QLabel {{
    color: {fg};
    background: transparent;
    font-size: 14px;
}}
DatePicker QPushButton {{
    color: {fg};
    background: transparent;
    border: none;
    font-size: 10px;
}}
""")

    def paintEvent(self, e):
        pass
