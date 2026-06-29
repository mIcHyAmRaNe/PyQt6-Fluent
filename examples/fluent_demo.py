"""Demo: all Fluent 2 components in a single window."""

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from pyqt_fluent import (
    Avatar,
    Badge,
    Button,
    Card,
    CheckBox,
    ComboBox,
    ContentDialog,
    DatePicker,
    Divider,
    Expander,
    FluentLabel,
    FluentTooltip,
    InfoBar,
    Input,
    NavigationView,
    NumberBox,
    ProgressBar,
    RadioButton,
    Rating,
    SearchBox,
    Slider,
    Spinner,
    Switch,
    TabView,
    Tag,
    Textarea,
    ThemeAwareWidget,
    ThemeDefinition,
    ThemeManager,
    TimePicker,
    ToggleButton,
)
from pyqt_fluent.utils.theme import Theme, system_theme


class Demo(ThemeAwareWidget, QWidget):
    qss_role = ""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fluent 2 Components")
        self.resize(900, 700)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        outer.addWidget(scroll)
        self.scroll = scroll

        container = QWidget()
        scroll.setWidget(container)
        self.container = container
        layout = QVBoxLayout(container)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # ── Section: Buttons ──
        layout.addWidget(FluentLabel("Buttons", "subtitle"))

        row = QHBoxLayout()
        row.addWidget(Button("Standard"))
        row.addWidget(Button("Accent", kind=Button.Kind.ACCENT))
        row.addWidget(Button("Transparent", kind=Button.Kind.TRANSPARENT))
        row.addWidget(Button("Text", kind=Button.Kind.TEXT))
        row.addWidget(Button("Outlined", kind=Button.Kind.OUTLINED))
        row.addWidget(Button("Filled", kind=Button.Kind.FILLED))
        row.addWidget(Button("", kind=Button.Kind.HYPERLINK))
        layout.addLayout(row)

        row2 = QHBoxLayout()
        row2.addWidget(ToggleButton("Toggle"))
        cb = CheckBox("Check me")
        cb.setChecked(True)
        row2.addWidget(cb)
        rb1 = RadioButton("Option A")
        rb2 = RadioButton("Option B")
        row2.addWidget(rb1)
        row2.addWidget(rb2)
        layout.addLayout(row2)

        # ── Section: Switch ──
        layout.addWidget(Divider())
        layout.addWidget(FluentLabel("Switch & Toggle", "subtitle"))
        row3 = QHBoxLayout()
        sw1 = Switch()
        sw1.setChecked(True)
        row3.addWidget(FluentLabel("Wi-Fi"))
        row3.addWidget(sw1)
        row3.addStretch()
        sw2 = Switch()
        row3.addWidget(FluentLabel("Bluetooth"))
        row3.addWidget(sw2)
        row3.addStretch()
        layout.addLayout(row3)

        # ── Section: Inputs ──
        layout.addWidget(Divider())
        layout.addWidget(FluentLabel("Inputs", "subtitle"))
        layout.addWidget(Input("Type here..."))
        layout.addWidget(SearchBox("Search..."))
        layout.addWidget(Textarea("Multi-line\ntext area"))

        row_slider = QHBoxLayout()
        sl = Slider()
        sl.set_value(0.65)
        row_slider.addWidget(FluentLabel("Volume"))
        row_slider.addWidget(sl)
        layout.addLayout(row_slider)

        row_tags = QHBoxLayout()
        row_tags.addWidget(Tag("Default"))
        t2 = Tag("Closable", closable=True)
        row_tags.addWidget(t2)
        t3 = Tag("Fluent", closable=True)
        row_tags.addWidget(t3)
        row_tags.addStretch()
        layout.addLayout(row_tags)

        row_rating = QHBoxLayout()
        rt = Rating()
        rt.set_value(3)
        row_rating.addWidget(FluentLabel("Rating:"))
        row_rating.addWidget(rt)
        row_rating.addStretch()
        layout.addLayout(row_rating)

        # ── Section: Feedback ──
        layout.addWidget(Divider())
        layout.addWidget(FluentLabel("Feedback", "subtitle"))
        row4 = QHBoxLayout()
        row4.addWidget(Spinner())
        row4.addWidget(Spinner(28))
        row4.addWidget(Spinner(36))
        row4.addStretch()
        layout.addLayout(row4)

        pb = ProgressBar()
        pb.set_value(0.6)
        layout.addWidget(pb)

        pb2 = ProgressBar()
        pb2.set_indeterminate(True)
        layout.addWidget(pb2)

        row5 = QHBoxLayout()
        row5.addWidget(Badge("3"))
        row5.addWidget(Badge("99+"))
        row5.addWidget(Badge())
        row5.addStretch()
        layout.addWidget(FluentLabel("Badges:"))
        layout.addLayout(row5)

        # ── Section: Cards ──
        layout.addWidget(Divider())
        layout.addWidget(FluentLabel("Cards & Layout", "subtitle"))
        grid = QHBoxLayout()
        for i in range(3):
            card = Card()
            cl = QVBoxLayout(card)
            cl.addWidget(FluentLabel(f"Card {i + 1}", "body_strong"))
            cl.addWidget(FluentLabel("Content goes here", "caption"))
            grid.addWidget(card)
        layout.addLayout(grid)

        # ── Section: Navigation ──
        layout.addWidget(Divider())
        layout.addWidget(FluentLabel("Navigation", "subtitle"))
        row_nav = QHBoxLayout()
        cb = ComboBox()
        cb.addItems(["Option A", "Option B", "Option C"])
        row_nav.addWidget(cb)
        row_nav.addWidget(DatePicker())
        row_nav.addWidget(TimePicker())
        row_nav.addWidget(NumberBox())
        row_nav.addStretch()
        layout.addLayout(row_nav)

        # TabView
        tabs = TabView()
        tabs.addTab(QWidget(), "Home")
        tabs.addTab(QWidget(), "Settings")
        layout.addWidget(tabs)

        # ── Section: Misc Widgets ──
        layout.addWidget(Divider())
        layout.addWidget(FluentLabel("Misc", "subtitle"))
        row_misc = QHBoxLayout()
        row_misc.addWidget(Avatar("JD", 40))
        row_misc.addWidget(Avatar("MK", 32))
        row_misc.addWidget(Avatar("A", 28))
        row_misc.addStretch()
        layout.addLayout(row_misc)

        # Expander
        exp = Expander("Show Details")
        exp.set_content(FluentLabel("Hidden content here"))
        layout.addWidget(exp)

        # InfoBar
        layout.addWidget(InfoBar("This is an info message", "info"))
        layout.addWidget(InfoBar("Operation successful!", "success"))
        layout.addWidget(InfoBar("Warning: check your input", "warning"))
        layout.addWidget(InfoBar("Error occurred", "danger"))

        # ── Theme toggle ──
        layout.addWidget(Divider())
        theme_btn = Button("Switch to Dark")
        layout.addWidget(theme_btn)

        self._theme_btn = theme_btn
        theme_btn.clicked.connect(self._toggle)
        self._init_theme_aware()

        # Detect system theme initially
        if system_theme() == Theme.DARK:
            ThemeManager.instance().set_dark_theme()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        bg = r.color("component.window_bg")
        fg = r.color("component.window_fg")
        p = self.palette()
        p.setColor(self.backgroundRole(), bg)
        p.setColor(self.foregroundRole(), fg)
        self.setPalette(p)
        self.setAutoFillBackground(True)
        self.scroll.setStyleSheet(f"QScrollArea {{ background-color: {bg.name()}; }}")
        self.container.setStyleSheet(f"background-color: {bg.name()}; color: {fg.name()};")

    def _toggle(self):
        mgr = ThemeManager.instance()
        mgr.toggle_theme()
        is_dark = mgr.theme().is_dark
        self._theme_btn.setText("Switch to Light" if is_dark else "Switch to Dark")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    d = Demo()
    d.show()
    app.exec()
