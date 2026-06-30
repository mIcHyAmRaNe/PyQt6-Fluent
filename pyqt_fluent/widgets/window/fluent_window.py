"""FluentWindow — ready-to-use main window with title bar + theme toggle."""

from __future__ import annotations

from PyQt6.QtWidgets import QMainWindow, QWidget

from ...tokens.theme import ThemeManager
from .frameless_window import FramelessWindow


class FluentWindow(QMainWindow, FramelessWindow):
    """A Fluent Design main window with integrated title bar and theme toggle."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._theme_btn = None
        self._tm = ThemeManager.instance()

    def set_content_widget(self, widget: QWidget):
        """Replace the central widget."""
        self.setCentralWidget(widget)
        self.title_bar.raise_()

    def _on_system_theme_changed(self):
        super()._on_system_theme_changed()
        self.title_bar.raise_()
