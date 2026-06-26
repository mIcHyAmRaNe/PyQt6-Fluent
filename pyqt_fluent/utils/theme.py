from enum import Enum


class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"


def system_theme():
    import winreg
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return Theme.DARK if value == 0 else Theme.LIGHT
    except Exception:
        return Theme.LIGHT


def is_dark():
    return system_theme() == Theme.DARK


def is_light():
    return system_theme() == Theme.LIGHT
