# coding:utf-8
import sys

from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QHBoxLayout

from pyqt_fluent import FramelessWindow, StandardTitleBar
from pyqt_fluent.webengine import FramelessWebEngineView


class Window(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # change the default title bar if you like
        self.set_title_bar(StandardTitleBar(self))

        self.h_box_layout = QHBoxLayout(self)

        # must replace QWebEngineView with FramelessWebEngineView
        self.web_engine = FramelessWebEngineView(self)

        self.h_box_layout.setContentsMargins(0, self.title_bar.height(), 0, 0)
        self.h_box_layout.addWidget(self.web_engine)

        # load web page
        self.web_engine.load(QUrl("https://michyamrane.github.io/"))
        self.resize(1200, 800)

        self.title_bar.raise_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    app.exec()
