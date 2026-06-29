"""Color utilities — HSV accent derivation matching qfluentwidgets ThemeColor."""

from __future__ import annotations

from PyQt6.QtGui import QColor


def derive_accent_variants(base: QColor, is_dark: bool) -> dict:
    """Derive accent hover/pressed from a base accent colour.

    Matches qfluentwidgets ``ThemeColor`` HSV logic:
      - Dark mode:  saturation * 0.84,  value fixed at 1.0  (colour pops)
      - Light mode: saturation * 1.0,   value * 0.75
    """
    h, s, v, _ = base.getHsvF()

    if is_dark:
        s *= 0.84
        v = 1.0
        rest = QColor.fromHsvF(h, min(s, 1.0), min(v, 1.0))
        hover = QColor.fromHsvF(h, min(s * 0.92, 1.0), min(v * 1.0, 1.0))
        pressed = QColor.fromHsvF(
            h, min(s * 0.977, 1.0), min(v * 0.90, 1.0)
        )
    else:
        rest = QColor.fromHsvF(h, min(s, 1.0), min(v, 1.0))
        hover = QColor.fromHsvF(h, min(s * 1.05, 1.0), min(v * 0.75, 1.0))
        pressed = QColor.fromHsvF(
            h, min(s * 1.05, 1.0), min(v * 0.50, 1.0)
        )

    return {"rest": rest, "hover": hover, "pressed": pressed}
