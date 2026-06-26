import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWebEngineWidgets import QWebEngineView

from .. import AcrylicWindow, FramelessWindow


class FramelessWebEngineView(QWebEngineView):
    def __init__(self, parent):
        if sys.platform == "win32" and isinstance(parent.window(), AcrylicWindow):
            parent.window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        super().__init__(parent=parent)
        if sys.platform in ("win32", "darwin"):
            self.setHtml("")
        if isinstance(self.window(), FramelessWindow):
            self.window().update_frameless()
