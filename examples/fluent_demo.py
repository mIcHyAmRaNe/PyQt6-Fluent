"""Demo: all Fluent 2 components in a single window."""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSplitter,
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
from pyqt_fluent.icons.engine import FluentIcon
from pyqt_fluent.icons.widget import IconWidget
from pyqt_fluent.utils.theme import Theme, system_theme


class Demo(ThemeAwareWidget, QWidget):
    qss_role = ""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fluent 2 Components")
        self.resize(1100, 750)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── CommandBar at top ──
        from pyqt_fluent import CommandBar

        cmd = CommandBar()
        cmd.add_action("New", icon=FluentIcon.NEW, callback=lambda: print("New"))
        cmd.add_action("Open", icon=FluentIcon.OPEN, callback=lambda: print("Open"))
        cmd.add_action("Save", icon=FluentIcon.SAVE, callback=lambda: print("Save"))
        cmd.add_separator()
        cmd.add_action("Undo", icon=FluentIcon.ARROW_UNDO, callback=lambda: print("Undo"))
        cmd.add_action("Redo", icon=FluentIcon.ARROW_REDO, callback=lambda: print("Redo"))
        cmd.add_stretch()
        cmd.add_action("Settings", icon=FluentIcon.SETTINGS, callback=lambda: print("Settings"))
        outer.addWidget(cmd)

        # ── Splitter: NavView | TabView ──
        splitter = QSplitter(Qt.Orientation.Horizontal)
        outer.addWidget(splitter, 1)

        # ── Sidebar ──
        self.nav = NavigationView()
        self.nav.add_item("Controls", icon=FluentIcon.HOME)
        self.nav.add_item("Status", icon=FluentIcon.STATUS)
        self.nav.add_item("Icons", icon=FluentIcon.ADD_SQUARE)
        self.nav.add_item("Misc", icon=FluentIcon.SETTINGS)
        self.nav.add_item("About", icon=FluentIcon.INFO)
        self.nav.set_current_index(0)
        self.nav.current_changed.connect(self._on_nav_changed)
        splitter.addWidget(self.nav)

        # ── Tabs ──
        self.tabs = TabView()
        splitter.addWidget(self.tabs)

        # Controls tab
        controls_tab = QWidget()
        controls_tab.setObjectName("tabControls")
        controls_layout = QVBoxLayout(controls_tab)
        controls_layout.setSpacing(12)
        controls_layout.setContentsMargins(16, 16, 16, 16)

        scroll_ctrl = QScrollArea()
        scroll_ctrl.setWidgetResizable(True)
        scroll_ctrl.setFrameShape(QFrame.Shape.NoFrame)
        scroll_ctrl.setWidget(controls_tab)
        self.tabs.addTab(scroll_ctrl, "Controls")

        # Buttons
        controls_layout.addWidget(FluentLabel("Buttons", "subtitle"))
        row = QHBoxLayout()
        row.addWidget(Button("Standard"))
        row.addWidget(Button("Accent", kind=Button.Kind.ACCENT))
        row.addWidget(Button("Transparent", kind=Button.Kind.TRANSPARENT))
        row.addWidget(Button("Filled", kind=Button.Kind.FILLED))
        row.addWidget(Button("Outlined", kind=Button.Kind.OUTLINED))
        row.addWidget(Button("Text", kind=Button.Kind.TEXT))
        row.addWidget(Button("", kind=Button.Kind.HYPERLINK))
        controls_layout.addLayout(row)

        controls_layout.addWidget(Divider())

        # Toggle + Selection
        row2 = QHBoxLayout()
        row2.addWidget(ToggleButton("Toggle"))
        cb = CheckBox("Check me")
        cb.setChecked(True)
        row2.addWidget(cb)
        rb1 = RadioButton("Option A")
        rb2 = RadioButton("Option B")
        rb1.setChecked(True)
        row2.addWidget(rb1)
        row2.addWidget(rb2)
        row2.addStretch()
        controls_layout.addLayout(row2)

        # Switch
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
        controls_layout.addLayout(row3)

        controls_layout.addWidget(Divider())

        # Inputs
        controls_layout.addWidget(FluentLabel("Inputs & Data", "subtitle"))
        controls_layout.addWidget(Input("Type here..."))
        controls_layout.addWidget(SearchBox("Search..."))
        controls_layout.addWidget(Textarea("Multi-line\ntext area"))

        row_in = QHBoxLayout()
        cb = ComboBox()
        cb.addItems(["Option A", "Option B", "Option C"])
        row_in.addWidget(cb)
        row_in.addWidget(DatePicker())
        row_in.addWidget(TimePicker())
        row_in.addWidget(NumberBox())
        row_in.addStretch()
        controls_layout.addLayout(row_in)

        # Slider
        row_sl = QHBoxLayout()
        sl = Slider()
        sl.set_value(0.65)
        row_sl.addWidget(FluentLabel("Volume"))
        row_sl.addWidget(sl)
        controls_layout.addLayout(row_sl)

        # Tags + Rating
        row_tr = QHBoxLayout()
        row_tr.addWidget(Tag("Default"))
        row_tr.addWidget(Tag("Closable", closable=True))
        rt = Rating()
        rt.set_value(3)
        row_tr.addWidget(FluentLabel("Rating:"))
        row_tr.addWidget(rt)
        row_tr.addStretch()
        controls_layout.addLayout(row_tr)

        # ── Status tab ──
        self._status_widget = QWidget()
        self._status_widget.setObjectName("tabStatus")
        status_layout = QVBoxLayout(self._status_widget)
        status_layout.setSpacing(12)
        status_layout.setContentsMargins(16, 16, 16, 16)

        scroll_st = QScrollArea()
        scroll_st.setWidgetResizable(True)
        scroll_st.setFrameShape(QFrame.Shape.NoFrame)
        scroll_st.setWidget(self._status_widget)
        self.tabs.addTab(scroll_st, "Status")

        status_layout.addWidget(FluentLabel("Spinners", "subtitle"))
        row_sp = QHBoxLayout()
        row_sp.addWidget(Spinner())
        row_sp.addWidget(Spinner(28))
        row_sp.addWidget(Spinner(36))
        row_sp.addStretch()
        status_layout.addLayout(row_sp)

        status_layout.addWidget(Divider())
        status_layout.addWidget(FluentLabel("Progress", "subtitle"))
        pb1 = ProgressBar()
        pb1.set_value(0.6)
        status_layout.addWidget(pb1)
        pb2 = ProgressBar()
        pb2.set_indeterminate(True)
        status_layout.addWidget(pb2)

        status_layout.addWidget(Divider())
        status_layout.addWidget(FluentLabel("Badges", "subtitle"))
        row_b = QHBoxLayout()
        row_b.addWidget(Badge("3"))
        row_b.addWidget(Badge("99+"))
        row_b.addWidget(Badge())
        row_b.addStretch()
        status_layout.addLayout(row_b)

        status_layout.addWidget(Divider())
        status_layout.addWidget(FluentLabel("InfoBar Notifications", "subtitle"))
        status_layout.addWidget(InfoBar("This is an info message", "info"))
        status_layout.addWidget(InfoBar("Operation successful!", "success"))
        status_layout.addWidget(InfoBar("Warning: check your input", "warning"))
        status_layout.addWidget(InfoBar("Error occurred", "danger"))

        # ── Icons tab ──
        icons_widget = QWidget()
        icons_widget.setObjectName("tabIcons")
        icons_layout = QVBoxLayout(icons_widget)
        icons_layout.setSpacing(12)
        icons_layout.setContentsMargins(16, 16, 16, 16)

        scroll_ic = QScrollArea()
        scroll_ic.setWidgetResizable(True)
        scroll_ic.setFrameShape(QFrame.Shape.NoFrame)
        scroll_ic.setWidget(icons_widget)
        self.tabs.addTab(scroll_ic, "Icons")

        icons_layout.addWidget(FluentLabel("Icons", "subtitle"))

        cols = 8
        icon_list = list(FluentIcon)
        for i in range(0, len(icon_list), cols):
            row_lay = QHBoxLayout()
            for icon_enum in icon_list[i:i + cols]:
                cell = QWidget()
                cell_lay = QVBoxLayout(cell)
                cell_lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell_lay.setSpacing(4)
                iw = IconWidget(icon_name=icon_enum, size=28)
                cell_lay.addWidget(iw)
                lbl = QLabel(icon_enum.name.replace("_", " ").title())
                lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell_lay.addWidget(lbl)
                row_lay.addWidget(cell)
            row_lay.addStretch()
            icons_layout.addLayout(row_lay)

        icons_layout.addStretch()

        # ── Misc tab ──
        self._misc_widget = QWidget()
        self._misc_widget.setObjectName("tabMisc")
        misc_layout = QVBoxLayout(self._misc_widget)
        misc_layout.setSpacing(12)
        misc_layout.setContentsMargins(16, 16, 16, 16)

        scroll_misc = QScrollArea()
        scroll_misc.setWidgetResizable(True)
        scroll_misc.setFrameShape(QFrame.Shape.NoFrame)
        scroll_misc.setWidget(self._misc_widget)
        self.tabs.addTab(scroll_misc, "Misc")

        # Cards
        misc_layout.addWidget(FluentLabel("Cards", "subtitle"))
        grid = QHBoxLayout()
        for i in range(3):
            card = Card()
            cl = QVBoxLayout(card)
            cl.addWidget(FluentLabel(f"Card {i + 1}", "body_strong"))
            cl.addWidget(FluentLabel("Content here", "caption"))
            grid.addWidget(card)
        misc_layout.addLayout(grid)

        # Avatar
        misc_layout.addWidget(Divider())
        misc_layout.addWidget(FluentLabel("Avatars", "subtitle"))
        row_a = QHBoxLayout()
        row_a.addWidget(Avatar("JD", 40))
        row_a.addWidget(Avatar("MK", 32))
        row_a.addWidget(Avatar("AB", 28))
        row_a.addWidget(Avatar("S", 24))
        row_a.addStretch()
        misc_layout.addLayout(row_a)

        # Expander
        misc_layout.addWidget(Divider())
        misc_layout.addWidget(FluentLabel("Expander", "subtitle"))
        exp = Expander("Show Details")
        exp.set_content(FluentLabel("Hidden content here"))
        misc_layout.addWidget(exp)

        exp2 = Expander("Preferences")
        inner = QWidget()
        inner_layout = QVBoxLayout(inner)
        inner_layout.addWidget(CheckBox("Enable notifications"))
        inner_layout.addWidget(CheckBox("Auto-save"))
        exp2.set_content(inner)
        misc_layout.addWidget(exp2)

        # ContentDialog trigger
        misc_layout.addWidget(Divider())
        misc_layout.addWidget(FluentLabel("Dialogs & Tooltips", "subtitle"))
        dialog_btn = Button("Open Content Dialog", kind=Button.Kind.ACCENT)
        dialog_btn.clicked.connect(self._show_dialog)
        misc_layout.addWidget(dialog_btn)

        # Tooltip trigger
        tip_btn = Button("Hover for tooltip")
        _tip = FluentTooltip("Hello from Fluent!")
        tip_btn.enterEvent = lambda e, t=_tip, b=tip_btn: t.show_for(b, "Hello from Fluent!", 2000)
        misc_layout.addWidget(tip_btn)

        misc_layout.addStretch()

        # ── About tab ──
        about_widget = QWidget()
        about_widget.setObjectName("tabAbout")
        about_layout = QVBoxLayout(about_widget)
        about_layout.setContentsMargins(32, 32, 32, 32)
        about_layout.addWidget(FluentLabel("PyQt6-Fluent", "title"))
        about_layout.addWidget(FluentLabel("A Fluent Design component library for PyQt6", "body"))
        about_layout.addWidget(FluentLabel("Version 0.1.0", "caption"))
        about_layout.addStretch()
        scroll_ab = QScrollArea()
        scroll_ab.setWidgetResizable(True)
        scroll_ab.setFrameShape(QFrame.Shape.NoFrame)
        scroll_ab.setWidget(about_widget)
        self.tabs.addTab(scroll_ab, "About")

        # ── Theme toggle ──
        outer.addWidget(Divider())
        theme_bar = QWidget()
        theme_bar.setObjectName("themeBar")
        theme_row = QHBoxLayout(theme_bar)
        theme_row.setContentsMargins(16, 8, 16, 8)
        self._theme_btn = Button("Switch to Dark")
        theme_row.addStretch()
        theme_row.addWidget(self._theme_btn)
        self._theme_btn.clicked.connect(self._toggle)
        outer.addWidget(theme_bar)

        self._init_theme_aware()

        if system_theme() == Theme.DARK:
            ThemeManager.instance().set_dark_theme()

    def _on_nav_changed(self, index: int):
        self.tabs.setCurrentIndex(index)

    def _show_dialog(self):
        dlg = ContentDialog(
            title="Confirm",
            message="Are you sure you want to proceed?",
            primary_text="OK",
            cancel_text="Cancel",
        )
        dlg.accepted.connect(lambda: print("Accepted"))
        dlg.rejected.connect(lambda: print("Rejected"))
        dlg.exec_()

    def _show_about(self):
        ContentDialog(
            title="About",
            message="PyQt6-Fluent v0.1.0\nA Fluent Design library.",
            primary_text="OK",
        ).exec_()

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        r = theme.resolver()
        bg = r.color("component.window_bg")
        fg = r.color("component.window_fg")
        card_bg = r.color("component.content_bg")
        border = r.color("component.border")
        nav_bg = r.color("component.nav_bg")
        nav_fg = r.color("component.nav_fg")
        input_bg = r.color("component.input_bg")
        input_fg = r.color("component.input_fg")
        input_border = r.color("component.input_border")
        accent = r.color("semantic.accent")
        on_accent = r.color("semantic.on_accent")
        hover = r.color("component.nav_item_hover")
        selected_bg = r.color("component.nav_selected_bg")
        selected_fg = r.color("component.nav_selected_fg")

        p = self.palette()
        p.setColor(self.backgroundRole(), bg)
        p.setColor(self.foregroundRole(), fg)
        self.setPalette(p)
        self.setAutoFillBackground(True)

        bg_hex = bg.name()
        fg_hex = fg.name()
        card_hex = card_bg.name()
        border_hex = border.name()
        nav_bg_hex = nav_bg.name()
        nav_fg_hex = nav_fg.name()
        input_bg_hex = input_bg.name()
        input_fg_hex = input_fg.name()
        input_border_hex = input_border.name()
        accent_hex = accent.name()
        on_accent_hex = on_accent.name()
        hover_hex = hover.name()

        # Get switch colors
        switch_track_off = r.color("component.switch_track_off").name()
        switch_track_on = r.color("component.switch_track_on").name()
        switch_thumb = r.color("component.switch_thumb").name()
        switch_thumb_size = r.int("component.switch_thumb_size")

        # Pre-compute semantic colors for QSS
        info_color = r.color("semantic.info").name()
        success_color = r.color("semantic.success").name()
        warning_color = r.color("semantic.warning").name()
        danger_color = r.color("semantic.danger").name()
        accent_hover = r.color("semantic.accent_hover").name()
        control_fg = r.color("semantic.control_fg").name()
        on_surface_muted = r.color("semantic.on_surface_muted").name()

        qss = f"""
/* Window & Container Backgrounds */
Demo, QSplitter {{
    background-color: {bg_hex};
    color: {fg_hex};
}}

/* Splitter Handle */
QSplitter::handle {{
    background-color: {border_hex};
    width: 1px;
}}

/* Scroll Areas */
QScrollArea {{
    background-color: transparent;
    border: none;
}}

QScrollArea > QWidget > QWidget {{
    background-color: transparent;
}}

/* NavigationView */
NavigationView {{
    background-color: {nav_bg_hex};
    color: {nav_fg_hex};
    border-right: 1px solid {border_hex};
}}

/* TabView */
TabView {{
    background-color: {card_hex};
    border: 1px solid {border_hex};
    border-radius: 4px;
}}

TabView::pane {{
    background-color: {card_hex};
    border: none;
}}

TabView QTabBar {{
    background-color: {card_hex};
    border-bottom: 1px solid {border_hex};
    padding: 0px;
    margin: 0px;
}}

TabView QTabBar::tab {{
    background-color: transparent;
    color: {fg_hex};
    padding: 8px 16px;
    border: none;
    border-bottom: 2px solid transparent;
    min-width: 80px;
    height: 36px;
}}

TabView QTabBar::tab:selected {{
    background-color: {card_hex};
    color: {accent_hex};
    border-bottom: 2px solid {accent_hex};
}}

TabView QTabBar::tab:hover {{
    background-color: {hover_hex};
}}

/* Cards */
Card {{
    background-color: {card_hex};
    border: 1px solid {border_hex};
    border-radius: 4px;
    padding: 12px;
}}

/* Input Fields */
Input, SearchBox, Textarea {{
    background-color: {input_bg_hex};
    color: {input_fg_hex};
    border: 1px solid {input_border_hex};
    border-radius: 4px;
    padding: 6px 10px;
    min-height: 32px;
}}

Input:focus, SearchBox:focus, Textarea:focus {{
    border: 2px solid {accent_hex};
    padding: 5px 9px;
}}

/* Bottom Theme Bar */
QWidget#themeBar {{
    background-color: {card_hex};
    border-top: 1px solid {border_hex};
}}

/* Progress Bars */
ProgressBar {{
    background-color: {input_bg_hex};
    border: 1px solid {border_hex};
    border-radius: 4px;
    text-align: center;
    min-height: 8px;
}}

ProgressBar::chunk {{
    background-color: {accent_hex};
    border-radius: 3px;
}}

/* InfoBars */
InfoBar {{
    background-color: {card_hex};
    border-left: 4px solid {accent_hex};
    border-radius: 0px;
    padding: 8px 16px;
    margin: 4px 0;
}}

InfoBar.info {{
    border-left-color: {info_color};
}}

InfoBar.success {{
    border-left-color: {success_color};
}}

InfoBar.warning {{
    border-left-color: {warning_color};
}}

InfoBar.danger {{
    border-left-color: {danger_color};
}}

/* CommandBar */
CommandBar {{
    background-color: {card_hex};
    border-bottom: 1px solid {border_hex};
    padding: 8px 16px;
}}

/* Buttons */
Button {{
    border-radius: 4px;
    padding: 6px 16px;
    font-size: 14px;
    min-height: 32px;
}}

/* ToggleButton */
ToggleButton {{
    border-radius: 4px;
    padding: 6px 16px;
    font-size: 14px;
    min-height: 32px;
}}

/* ComboBox */
ComboBox {{
    background-color: {input_bg_hex};
    color: {input_fg_hex};
    border: 1px solid {input_border_hex};
    border-radius: 4px;
    padding: 6px 10px;
    min-height: 32px;
}}

ComboBox:focus {{
    border: 2px solid {accent_hex};
    padding: 5px 9px;
}}

/* DatePicker, TimePicker, NumberBox */
DatePicker, TimePicker, NumberBox {{
    background-color: {input_bg_hex};
    color: {input_fg_hex};
    border: 1px solid {input_border_hex};
    border-radius: 4px;
    padding: 6px 10px;
    min-height: 32px;
}}

DatePicker:focus, TimePicker:focus, NumberBox:focus {{
    border: 2px solid {accent_hex};
    padding: 5px 9px;
}}

/* Slider */
Slider {{
    background-color: {input_bg_hex};
    border-radius: 4px;
}}

Slider::groove {{
    background-color: {input_bg_hex};
    border: 1px solid {border_hex};
    border-radius: 4px;
    height: 8px;
}}

Slider::handle {{
    background-color: {accent_hex};
    border-radius: 8px;
    width: 16px;
    height: 16px;
    margin: -4px 0;
}}

Slider::add-page {{
    background-color: {accent_hex};
    border-radius: 4px;
}}

Slider::sub-page {{
    background-color: {input_bg_hex};
    border-radius: 4px;
}}

/* Rating */
Rating {{
    background-color: transparent;
}}

/* CheckBox */
CheckBox {{
    spacing: 8px;
}}

CheckBox::indicator {{
    background-color: transparent;
    border: 2px solid {border_hex};
    border-radius: 4px;
    width: 18px;
    height: 18px;
}}

CheckBox::indicator:checked {{
    background-color: {accent_hex};
    border-color: {accent_hex};
}}

CheckBox::indicator:checked:hover {{
    background-color: {accent_hover};
}}

/* RadioButton */
RadioButton {{
    spacing: 8px;
}}

RadioButton::indicator {{
    background-color: transparent;
    border: 2px solid {border_hex};
    border-radius: 9px;
    width: 18px;
    height: 18px;
}}

RadioButton::indicator:checked {{
    background-color: {accent_hex};
    border-color: {accent_hex};
}}

RadioButton::indicator:checked:hover {{
    background-color: {accent_hover};
}}

/* Expander */
Expander {{
    background-color: transparent;
    border: 1px solid {border_hex};
    border-radius: 4px;
    padding: 8px 12px;
}}

Expander:hover {{
    background-color: {hover_hex};
}}

/* Badge */
Badge {{
    background-color: {accent_hex};
    color: {on_accent_hex};
    border-radius: 8px;
    padding: 2px 8px;
    font-size: 12px;
    font-weight: 600;
}}

/* Tag */
Tag {{
    background-color: {card_hex};
    color: {fg_hex};
    border: 1px solid {border_hex};
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
}}

/* Spinner */
Spinner {{
    background-color: transparent;
}}

/* Avatar */
Avatar {{
    border-radius: 50%;
}}

/* Divider */
Divider {{
    background-color: {border_hex};
    height: 1px;
    margin: 8px 0;
}}

/* Label styling */
FluentLabel {{
    background-color: transparent;
    color: {fg_hex};
}}

FluentLabel[level="title"] {{
    font-size: 24px;
    font-weight: 600;
}}

FluentLabel[level="subtitle"] {{
    font-size: 18px;
    font-weight: 600;
    color: {fg_hex};
    margin-bottom: 8px;
}}

FluentLabel[level="body"] {{
    font-size: 14px;
    color: {fg_hex};
}}

FluentLabel[level="body_strong"] {{
    font-size: 14px;
    font-weight: 600;
    color: {fg_hex};
}}

FluentLabel[level="caption"] {{
    font-size: 12px;
    color: {on_surface_muted};
}}
"""
        self.setStyleSheet(qss)

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
