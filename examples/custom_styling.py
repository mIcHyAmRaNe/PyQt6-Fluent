"""Full customization: copy a theme preset, override component tokens and semantic refs."""

import sys

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout

from pyqt_fluent import FramelessWindow, StandardTitleBar, ThemeManager
from pyqt_fluent.tokens import ThemeDefinition, ThemeMode
from pyqt_fluent.tokens.component import ComponentTokens
from pyqt_fluent.tokens.typography import Typography


class CustomWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.set_title_bar(StandardTitleBar(self))
        self.setWindowTitle("Custom Styling")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Fully Customized Window")
        title.setObjectName("demoTitle")
        title.setStyleSheet(
            "font-size: 22px; font-weight: 700; color: #7C5CFC; background: transparent;"
        )
        layout.addWidget(title)

        desc = QLabel(
            "Custom corner radius (16px), titlebar & window colours,\n"
            "custom font stack, accent colour — all via ThemeDefinition."
        )
        desc.setObjectName("demoDesc")
        desc.setStyleSheet(
            "font-size: 13px; color: #A0A0C0; padding: 4px 0; background: transparent;"
        )
        layout.addWidget(desc)

        layout.addStretch()
        self.title_bar.raise_()
        self.resize(520, 380)

        self._apply_custom_theme()

    def _apply_custom_theme(self):
        base = ThemeManager.instance().theme()
        custom = ThemeDefinition(
            name="Custom",
            mode=ThemeMode.LIGHT,
            palette=base.palette,
            semantic=base.semantic,
            component=ComponentTokens(
                window_radius=16,
                control_radius=8,
                titlebar_height=40,
            ),
            typography=Typography(
                fontFamily="Segoe UI Variable",
                fallbackFamilies=["Segoe UI", "Consolas"],
            ),
        )
        ThemeManager.instance().set_theme(custom)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = CustomWindow()
    demo.show()
    sys.exit(app.exec())
