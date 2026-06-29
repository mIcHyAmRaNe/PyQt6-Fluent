from __future__ import annotations

from ...styles.engine import StylesheetEngine
from ...tokens.theme import ThemeDefinition, ThemeManager


class ThemeAwareWidget:
    """Mixin for widgets that respond to theme changes.

    Subclasses declare::
        qss_role = "PushButton"   # key into _BUILT_INS in engine.py

    Then call ``self._init_theme_aware()`` at the end of ``__init__``.
    Override ``on_theme_applied(theme)`` for non-QSS updates (icon colors,
    custom painter state, etc.).

    No manual unregister needed — ``ThemeManager`` uses a ``WeakSet``.
    """

    qss_role: str = ""

    def _init_theme_aware(self) -> None:
        tm = ThemeManager.instance()
        tm.register_observer(self)
        self._apply_theme(tm.theme())

    def on_theme_changed(self, theme: ThemeDefinition) -> None:
        self._apply_theme(theme)

    def _apply_theme(self, theme: ThemeDefinition) -> None:
        if self.qss_role:
            self.setStyleSheet(StylesheetEngine.for_role(self.qss_role, theme))
        self.on_theme_applied(theme)

    def on_theme_applied(self, theme: ThemeDefinition) -> None:
        pass
