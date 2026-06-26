from PyQt6.QtCore import QEvent, Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from ...tokens.theme import ThemeDefinition, ThemeManager, ThemeObserver
from ...utils import start_system_move, toggle_max_state
from .title_bar_buttons import (  # noqa: F401
    CloseButton,
    MaximizeButton,
    MinimizeButton,
    SvgTitleBarButton,
    TitleBarButton,
)


class TitleBarBase(QWidget, ThemeObserver):
    def __init__(self, parent):
        super().__init__(parent)
        self.min_btn = MinimizeButton(parent=self)
        self.close_btn = CloseButton(parent=self)
        self.max_btn = MaximizeButton(parent=self)

        self._is_double_click_enabled = True
        self._tm = ThemeManager.instance()

        self.resize(200, 32)
        self.setFixedHeight(32)

        self.min_btn.clicked.connect(self.window().showMinimized)
        self.max_btn.clicked.connect(self._toggle_max_state)
        self.close_btn.clicked.connect(self.window().close)

        self.window().installEventFilter(self)
        self._tm.register_observer(self)
        self._apply_theme(self._tm.theme())

    def _apply_theme(self, theme: ThemeDefinition) -> None:
        bg = theme.color("component.titlebar_bg")
        self.setStyleSheet(f"TitleBarBase {{ background-color: {bg.name()}; }}")

    def on_theme_changed(self, theme: ThemeDefinition) -> None:
        self._apply_theme(theme)

    def eventFilter(self, obj, e):
        if obj is self.window() and e.type() == QEvent.Type.WindowStateChange:
            self.max_btn.set_max_state(self.window().isMaximized())
        return super().eventFilter(obj, e)

    def mouseDoubleClickEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton or not self._is_double_click_enabled:
            return
        self._toggle_max_state()

    def mouseMoveEvent(self, e):
        if not self.can_drag(e.pos()):
            return
        start_system_move(self.window(), e.globalPosition().toPoint())

    def mousePressEvent(self, e):
        if not self.can_drag(e.pos()):
            return
        start_system_move(self.window(), e.globalPosition().toPoint())

    def _toggle_max_state(self):
        toggle_max_state(self.window())

    def _is_drag_region(self, pos):
        width = sum(b.width() for b in self.findChildren(TitleBarButton) if b.isVisible())
        return 0 < pos.x() < self.width() - width

    def _has_button_pressed(self):
        return any(b.is_pressed() for b in self.findChildren(TitleBarButton))

    def can_drag(self, pos):
        return self._is_drag_region(pos) and not self._has_button_pressed()

    def set_double_click_enabled(self, is_enabled):
        self._is_double_click_enabled = is_enabled


class TitleBar(TitleBarBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.h_box_layout = QHBoxLayout(self)
        self.h_box_layout.setSpacing(0)
        self.h_box_layout.setContentsMargins(0, 0, 0, 0)
        self.h_box_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.h_box_layout.addStretch(1)
        self.h_box_layout.addWidget(self.min_btn, 0, Qt.AlignmentFlag.AlignRight)
        self.h_box_layout.addWidget(self.max_btn, 0, Qt.AlignmentFlag.AlignRight)
        self.h_box_layout.addWidget(self.close_btn, 0, Qt.AlignmentFlag.AlignRight)


class StandardTitleBar(TitleBar):
    def __init__(self, parent):
        self.icon_label = QLabel()
        self.title_label = QLabel()
        super().__init__(parent)

        self.icon_label.setParent(self)
        self.icon_label.setFixedSize(20, 20)
        self.h_box_layout.insertSpacing(0, 10)
        self.h_box_layout.insertWidget(1, self.icon_label, 0, Qt.AlignmentFlag.AlignLeft)
        self.window().windowIconChanged.connect(self.set_icon)

        self.title_label.setParent(self)
        self.h_box_layout.insertWidget(2, self.title_label, 0, Qt.AlignmentFlag.AlignLeft)
        self.window().windowTitleChanged.connect(self.set_title)
        self._style_title_label()

    def _style_title_label(self):
        theme = ThemeManager.instance().theme()
        fg = theme.color("component.titlebar_fg")
        ff = theme.typography.fontFamily
        self.title_label.setStyleSheet(f"""
            QLabel {{
                background: transparent;
                font-family: "{ff}";
                font-size: 13px;
                color: {fg.name()};
                padding: 0 4px;
            }}
        """)

    def _apply_theme(self, theme: ThemeDefinition) -> None:
        self._style_title_label()
        super()._apply_theme(theme)

    def set_title(self, title):
        self.title_label.setText(title)
        self.title_label.adjustSize()

    def set_icon(self, icon):
        self.icon_label.setPixmap(QIcon(icon).pixmap(20, 20))
