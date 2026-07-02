import warnings

from ..tokens.theme import ThemeMode


class Theme:
    """Deprecated — use ``ThemeMode`` from ``tokens.theme`` instead."""

    LIGHT = ThemeMode.LIGHT
    DARK = ThemeMode.DARK

    def __init_subclass__(cls, **kw):
        warnings.warn(
            "Theme is deprecated, use ThemeMode from pyqt_fluent.tokens.theme",
            DeprecationWarning,
            stacklevel=2,
        )


def system_theme():
    import winreg
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return ThemeMode.DARK if value == 0 else ThemeMode.LIGHT
    except Exception:
        return ThemeMode.LIGHT


def is_dark():
    return system_theme() == ThemeMode.DARK


def is_light():
    return system_theme() == ThemeMode.LIGHT
