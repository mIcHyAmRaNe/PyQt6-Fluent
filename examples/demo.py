"""Minimal frameless window — now with themed titlebar and live dark/light toggle."""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QHBoxLayout, QVBoxLayout

from pyqt_fluent import FramelessWindow, StandardTitleBar, ThemeManager


class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap = None

    def setPixmap(self, p):
        self._pixmap = p
        self.update()

    def paintEvent(self, e):
        if self._pixmap is None:
            return super().paintEvent(e)
        p = QPainter(self)
        scaled = self._pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        x = (self.width() - scaled.width()) // 2
        y = (self.height() - scaled.height()) // 2
        p.drawPixmap(x, y, scaled)
        p.end()


class Window(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.set_title_bar(StandardTitleBar(self))
        self.setWindowIcon(QIcon("assets/logo.svg"))
        self.setWindowTitle("PyQt-Frameless-Window")

        self.label = ImageLabel(self)
        self.label.setPixmap(QPixmap("assets/rezero.jpg"))

        # Theme toggle button
        self._theme_btn = QPushButton("Toggle Theme", self)
        self._theme_btn.setFixedSize(120, 30)
        self._theme_btn.clicked.connect(ThemeManager.instance().toggle_theme)

        self.title_bar.raise_()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        m = 10
        tb = self.title_bar
        self.label.setGeometry(
            m, tb.height() + m,
            self.width() - 2 * m,
            self.height() - tb.height() - 2 * m - 50,
        )
        self._theme_btn.move(
            self.width() - self._theme_btn.width() - 10,
            self.height() - self._theme_btn.height() - 10,
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Window()
    demo.resize(600, 450)
    demo.show()
    sys.exit(app.exec())
