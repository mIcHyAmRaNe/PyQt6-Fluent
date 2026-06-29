"""Visual test — all button widgets imported from pyqt_fluent."""

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from pyqt_fluent import (
    Button,
    CheckBox,
    FramelessWindow,
    RadioButton,
    StandardTitleBar,
    ThemeManager,
    ToggleButton,
)

_APPEARANCES = [
    ("Standard", Button.Kind.STANDARD),
    ("Accent", Button.Kind.ACCENT),
    ("Transparent", Button.Kind.TRANSPARENT),
    ("Text", Button.Kind.TEXT),
    ("Outlined", Button.Kind.OUTLINED),
    ("Hyperlink", Button.Kind.HYPERLINK),
    ("Filled", Button.Kind.FILLED),
]


class DemoWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.set_title_bar(StandardTitleBar(self))
        self.setWindowTitle("PyQt6-Fluent Button Demo")
        self.resize(720, 780)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        title = QLabel("PyQt6-Fluent Widgets — Win11 Buttons")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")
        root.addWidget(title)

        subtitle = QLabel(
            "7 PushButton variants + ToggleButton, CheckBox, RadioButton\n"
            "120ms bg fade, translate-Y, pressed-opacity 0.786, ripple, focus ring"
        )
        subtitle.setStyleSheet("font-size: 12px; color: #888;")
        root.addWidget(subtitle)

        # ── Button variants ──────────────────────────────────
        for group_name, kind in _APPEARANCES:
            group = QGroupBox(group_name)
            row = QHBoxLayout(group)
            row.setSpacing(8)
            for label in ["Rest", "Hover me", "Press me"]:
                btn = Button(label, kind=kind)
                btn.setFixedSize(110, 32)
                row.addWidget(btn)
            row.addStretch()
            root.addWidget(group)

        # ── ToggleButton ─────────────────────────────────────
        group = QGroupBox("ToggleButton")
        row = QHBoxLayout(group)
        for label in ["Toggle A", "Toggle B", "Toggle C"]:
            btn = ToggleButton(label)
            btn.setFixedSize(120, 32)
            row.addWidget(btn)
        row.addStretch()
        root.addWidget(group)

        # ── CheckBox ─────────────────────────────────────────
        group = QGroupBox("CheckBox")
        row = QHBoxLayout(group)
        for label in ["Apple", "Banana", "Cherry"]:
            cb = CheckBox(label)
            row.addWidget(cb)
        row.addStretch()
        root.addWidget(group)

        # ── RadioButton ──────────────────────────────────────
        group = QGroupBox("RadioButton")
        row = QHBoxLayout(group)
        rb_a = RadioButton("Option A")
        rb_b = RadioButton("Option B")
        rb_c = RadioButton("Option C")
        rb_a.setChecked(True)
        for rb in [rb_a, rb_b, rb_c]:
            row.addWidget(rb)
        row.addStretch()
        root.addWidget(group)

        # ── Toggle theme ─────────────────────────────────────
        row = QHBoxLayout()
        self._toggle = Button("Toggle Theme")
        self._toggle.clicked.connect(self._toggle_theme)
        row.addWidget(self._toggle)
        row.addStretch()
        root.addLayout(row)

        root.addStretch()
        self.title_bar.raise_()

    def _toggle_theme(self):
        ThemeManager.instance().toggle_theme()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DemoWindow()
    win.show()
    sys.exit(app.exec())
