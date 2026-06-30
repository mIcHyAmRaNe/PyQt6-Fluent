from __future__ import annotations

from PyQt6.QtCore import QEventLoop, QRectF, Qt, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPainterPath
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ...tokens.theme import ThemeDefinition
from .._shared.theme_aware import ThemeAwareWidget
from ..buttons import Button


class ContentDialog(ThemeAwareWidget, QWidget):
    accepted = pyqtSignal()
    rejected = pyqtSignal()

    def __init__(self, parent=None, title="", message="",
                 bg_color=None, overlay_color=None,
                 primary_text="OK", cancel_text="Cancel", radius=8):
        super().__init__(parent)
        self._title = title
        self._message = message
        self._primary_text = primary_text
        self._cancel_text = cancel_text
        self._custom_radius = radius

        self._bg = QColor()
        self._overlay = QColor()
        self._custom_bg = QColor(bg_color) if bg_color else None
        self._custom_overlay = QColor(overlay_color) if overlay_color else None

        self._loop: QEventLoop | None = None

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self._overlay_widget = QWidget(self)
        self._overlay_widget.setGeometry(0, 0, 0, 0)
        self._overlay_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self._overlay_widget.raise_()

        self._card = QWidget(self)
        self._card.setFixedWidth(420)
        self._card_layout = QVBoxLayout(self._card)
        self._card_layout.setContentsMargins(24, 24, 24, 24)
        self._card_layout.setSpacing(12)

        self._title_label = QLabel(title)
        title_font = QFont("Segoe UI Variable, Segoe UI, sans-serif")
        title_font.setPixelSize(20)
        title_font.setBold(True)
        self._title_label.setFont(title_font)
        self._card_layout.addWidget(self._title_label)

        self._message_label = QLabel(message)
        msg_font = QFont("Segoe UI Variable, Segoe UI, sans-serif")
        msg_font.setPixelSize(14)
        self._message_label.setFont(msg_font)
        self._message_label.setWordWrap(True)
        self._card_layout.addWidget(self._message_label)

        self._card_layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        btn_layout.addStretch()

        self._cancel_btn = Button(cancel_text, kind=Button.Kind.STANDARD)
        self._cancel_btn.clicked.connect(self._reject)
        btn_layout.addWidget(self._cancel_btn)

        self._primary_btn = Button(primary_text, kind=Button.Kind.ACCENT)
        self._primary_btn.clicked.connect(self._accept)
        btn_layout.addWidget(self._primary_btn)

        self._card_layout.addLayout(btn_layout)

        self._init_theme_aware()

    def _accept(self):
        self.accepted.emit()
        self._close_loop(True)

    def _reject(self):
        self.rejected.emit()
        self._close_loop(False)

    def _close_loop(self, _result: bool = True):
        if self._loop and self._loop.isRunning():
            self._loop.quit()
        self.close()

    def exec_(self):
        if self.parent():
            self.setGeometry(self.parent().rect())
        self.show()
        self._loop = QEventLoop()
        self._loop.exec()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._overlay_widget.setGeometry(self.rect())
        card_size = self._card.sizeHint()
        self._card.move(
            (self.width() - self._card.width()) // 2,
            (self.height() - card_size.height()) // 2,
        )

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        self._bg = self._custom_bg if self._custom_bg else r.color("component.contentdialog_bg")
        self._overlay = self._custom_overlay if self._custom_overlay else r.color("component.contentdialog_overlay")
        radius = self._custom_radius if self._custom_radius is not None else r.int("component.contentdialog_radius")

        self._card.setObjectName("dialogCard")
        self._card.setStyleSheet(f"""
            QWidget#dialogCard {{
                background-color: {self._bg.name()};
                border-radius: {radius}px;
            }}
        """)
        fg = r.color("semantic.on_surface").name()
        self._title_label.setStyleSheet(f"color: {fg}; background: transparent;")
        self._message_label.setStyleSheet(f"color: {fg}; background: transparent;")
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QBrush(self._overlay))

        card_rect = QRectF(self._card.geometry())
        radius = self._custom_radius if self._custom_radius is not None else 8
        path = QPainterPath()
        path.addRoundedRect(card_rect, radius, radius)
        painter.fillPath(path, QBrush(self._bg))
