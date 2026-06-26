# coding:utf-8
import sys

from PyQt6.QtWidgets import QApplication

from pyqt_fluent import FramelessWindow
from pyqt_fluent.utils import ScreenCaptureFilter


class Window(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("PyQt-Frameless-Window")

        # disable screen capture
        self.installEventFilter(ScreenCaptureFilter(self))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec())
