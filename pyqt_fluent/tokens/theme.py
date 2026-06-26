"""ThemeDefinition (combines all 3 tiers) + ThemeManager (singleton, signals, observers)."""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor

from .component import ComponentTokens
from .palette import Palette
from .resolver import TokenResolver
from .semantic import SemanticPalette
from .typography import Typography


class ThemeMode(Enum):
    LIGHT = "light"
    DARK = "dark"


@dataclass
class ThemeDefinition:
    name: str = "Light"
    mode: ThemeMode = ThemeMode.LIGHT
    palette: Palette = field(default_factory=Palette)
    semantic: SemanticPalette = field(default_factory=SemanticPalette)
    component: ComponentTokens = field(default_factory=ComponentTokens)
    typography: Typography = field(default_factory=Typography)

    @property
    def is_dark(self) -> bool:
        return self.mode == ThemeMode.DARK

    def resolver(self) -> TokenResolver:
        return TokenResolver(self.palette, self.semantic, self.component, self.is_dark)

    def resolve(self, path: str) -> Any:
        return self.resolver().resolve(path)

    def color(self, path: str) -> QColor:
        return self.resolver().color(path)

    def copy_with(self, **overrides: Any) -> ThemeDefinition:
        new = ThemeDefinition(
            name=overrides.pop("name", self.name),
            mode=overrides.pop("mode", self.mode),
            palette=self.palette,
            semantic=self.semantic,
            component=self.component,
            typography=self.typography,
        )
        for k, v in overrides.items():
            if hasattr(new.component, k):
                setattr(new.component, k, v)
        return new


class ThemeObserver(QObject):
    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)

    @abstractmethod
    def on_theme_changed(self, theme: ThemeDefinition) -> None: ...


class ThemeManager(QObject):
    themeChanged = pyqtSignal(ThemeDefinition)

    _instance: ThemeManager | None = None

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._theme: ThemeDefinition = ThemeDefinition()
        self._observers: list[ThemeObserver] = []

    @classmethod
    def instance(cls) -> ThemeManager:
        if cls._instance is None:
            cls._instance = ThemeManager()
            cls._instance._apply_system_theme()
        return cls._instance

    def _apply_system_theme(self) -> None:
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            )
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            if value == 0:
                self.set_dark_theme()
        except Exception:
            pass

    def set_theme(self, theme: ThemeDefinition) -> None:
        self._theme = theme
        self.themeChanged.emit(theme)
        for obs in list(self._observers):
            try:
                obs.on_theme_changed(theme)
            except RuntimeError:
                self._observers.remove(obs)

    def set_light_theme(self) -> None:
        import dataclasses

        from ..presets import LIGHT_THEME
        self.set_theme(dataclasses.replace(LIGHT_THEME))

    def set_dark_theme(self) -> None:
        import dataclasses

        from ..presets import DARK_THEME
        self.set_theme(dataclasses.replace(DARK_THEME))

    def toggle_theme(self) -> None:
        if self._theme.mode == ThemeMode.DARK:
            self.set_light_theme()
        else:
            self.set_dark_theme()

    def theme(self) -> ThemeDefinition:
        return self._theme

    def resolve(self, path: str) -> Any:
        return self._theme.resolve(path)

    def register_observer(self, observer: ThemeObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unregister_observer(self, observer: ThemeObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def generate_stylesheet(self) -> str:
        t = self._theme
        r = t.resolver()
        bg = r.color("component.window_bg").name()
        fg = r.color("component.window_fg").name()
        cb = r.color("component.content_bg").name()
        cf = r.color("component.content_fg").name()
        bo = r.color("component.border").name()
        cr = r.int("component.control_radius")
        bw = r.int("component.border_width")
        ff = t.typography.fontFamily
        fs = t.typography.body.size

        return f"""
        QWidget {{
            background-color: {bg};
            color: {fg};
            font-family: "{ff}";
            font-size: {fs}px;
        }}
        QLabel {{
            background: transparent;
            color: {cf};
        }}
        QPushButton {{
            background-color: {cb};
            color: {cf};
            border: {bw}px solid {bo};
            border-radius: {cr}px;
            padding: 4px 12px;
        }}
        QTextEdit, QLineEdit {{
            background-color: {cb};
            color: {cf};
            border: {bw}px solid {bo};
            border-radius: {cr}px;
        }}
        """
