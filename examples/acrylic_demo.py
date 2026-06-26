# coding:utf-8
"""Acrylic window — the blur gradient auto‑adapts to dark/light mode."""

import sys

from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout
from pyqt_fluent import AcrylicWindow


class Window(AcrylicWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Acrylic Window")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 50, 20, 20)
        layout.addWidget(
            QLabel(
                "Switch Windows 11 theme (Settings → Personalization → Colors)\n"
                "and watch the acrylic gradient, titlebar, and DWM follow along."
            )
        )

        self.title_bar.raise_()

    # Uncomment to use a custom tint (overrides auto‑theme):
    # self.window_effect.set_acrylic_effect(self.winId(), "106EBE99")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Window()
    demo.resize(500, 300)
    demo.show()
    sys.exit(app.exec())
