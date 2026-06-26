"""Catppuccin Frappé theme with a handwriting font — applied on startup."""

import sys

from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout

from pyqt_fluent import FramelessWindow, StandardTitleBar, ThemeManager
from pyqt_fluent.presets import CATPPUCCIN_FRAPPE


class CatppuccinWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.set_title_bar(StandardTitleBar(self))
        self.setWindowTitle("Catppuccin Frappé")

        ThemeManager.instance().set_theme(CATPPUCCIN_FRAPPE)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(12)

        title = QLabel("Catppuccin Frappé")
        title.setStyleSheet(
            "font-size: 26px; font-weight: 700; color: #ca9ee6; background: transparent;"
        )
        layout.addWidget(title)

        desc = QLabel(
            "a warm, soft dark palette with pastel accents\n"
            "handwriting font — Gabriola"
        )
        desc.setStyleSheet(
            "font-size: 14px; color: #b5bfe2; background: transparent;"
        )
        layout.addWidget(desc)

        info = QLabel(
            "Window bg  #f2d5cf\n"
            "Titlebar bg #eebebe\n"
            "Accent     #8caaee / #ca9ee6"
        )
        info.setStyleSheet(
            "font-size: 12px; color: #737994; background: transparent;"
        )
        layout.addWidget(info)

        layout.addStretch()
        self.title_bar.raise_()
        self.resize(460, 320)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.title_bar.raise_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = CatppuccinWindow()
    demo.show()
    sys.exit(app.exec())
