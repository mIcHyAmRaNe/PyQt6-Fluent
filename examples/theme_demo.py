"""Comprehensive demo showcasing the live theme engine and Win11 design language."""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from pyqt_fluent import (
    AcrylicWindow,
    FramelessWindow,
    StandardTitleBar,
    ThemeManager,
)
import dataclasses

from pyqt_fluent.presets import LIGHT_THEME, DARK_THEME



class ThemeSettingsPanel(QWidget):
    """Interactive panel demonstrating every customization API."""

    def __init__(self, window):
        super().__init__()
        self._window = window
        self._tm = ThemeManager.instance()

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Theme Designer")
        title.setStyleSheet("font-size: 20px; font-weight: 600; padding: 8px 0;")
        layout.addWidget(title)

        # ── Theme toggle ───────────────────────────────────────
        row = QHBoxLayout()
        row.addWidget(QLabel("Theme:"))
        self._theme_combo = QComboBox()
        self._theme_combo.addItems(["Light", "Dark"])
        self._theme_combo.currentTextChanged.connect(self._on_theme_changed)
        row.addWidget(self._theme_combo)
        layout.addLayout(row)

        # ── Corner radius ──────────────────────────────────────
        row = QHBoxLayout()
        row.addWidget(QLabel("Window Radius:"))
        self._radius_slider = QSlider(Qt.Orientation.Horizontal)
        self._radius_slider.setRange(0, 20)
        self._radius_slider.setValue(8)
        self._radius_slider.valueChanged.connect(self._on_radius_changed)
        row.addWidget(self._radius_slider)
        self._radius_label = QLabel("8px")
        row.addWidget(self._radius_label)
        layout.addLayout(row)

        # ── Actions ────────────────────────────────────────────
        row = QHBoxLayout()
        self._toggle_btn = QPushButton("Toggle Dark/Light")
        self._toggle_btn.clicked.connect(self._on_toggle_theme)
        row.addWidget(self._toggle_btn)

        self._reset_btn = QPushButton("Reset Defaults")
        self._reset_btn.clicked.connect(self._on_reset)
        row.addWidget(self._reset_btn)
        layout.addLayout(row)

        layout.addStretch()

        info = QLabel(
            "Windows 11 design: rounded corners, Segoe UI Variable font,\n"
            "consistent 4epx spacing, light/dark mode."
        )
        info.setStyleSheet("font-size: 12px; color: #888; padding-top: 12px;")
        layout.addWidget(info)

    def _on_theme_changed(self, name):
        if name == "Light":
            self._tm.set_theme(LIGHT_THEME)
        elif name == "Dark":
            self._tm.set_theme(DARK_THEME)

    def _on_radius_changed(self, v):
        self._radius_label.setText(f"{v}px")
        t = dataclasses.replace(
            self._tm.theme(),
            component=dataclasses.replace(self._tm.theme().component, window_radius=v),
        )
        self._tm.set_theme(t)

    def _on_toggle_theme(self):
        self._tm.toggle_theme()
        name = self._tm.theme().name
        self._theme_combo.blockSignals(True)
        self._theme_combo.setCurrentText(name)
        self._theme_combo.blockSignals(False)

    def _on_reset(self):
        self._tm.set_theme(LIGHT_THEME)
        self._radius_slider.setValue(8)
        self._theme_combo.setCurrentText("Light")


class ThemeDemoWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.set_title_bar(StandardTitleBar(self))
        self.setWindowTitle("PyQt-Frameless-Window — Theme Demo")
        self.resize(720, 600)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(ThemeSettingsPanel(self))
        root.addStretch()

        self.title_bar.raise_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = ThemeDemoWindow()
    demo.show()
    sys.exit(app.exec())
