from __future__ import annotations

from PyQt6.QtCore import QVariantAnimation

from ...utils.animation import winui_easing


class TranslateYAnimation:
    """Mixin for widgets that shift content down on press (Win11 style).

    Expects:
      - ``self.update()`` from QWidget
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._translate_y = 0.0
        self._ty_ani = QVariantAnimation(self)
        self._ty_ani.valueChanged.connect(self._on_ty_ani)

    # ── helpers ─────────────────────────────────────────────

    def _on_ty_ani(self, value: float) -> None:
        self._translate_y = float(value)
        self.update()

    def _start_press_translate(self, target: float = 1.0) -> None:
        self._ty_ani.stop()
        self._ty_ani.setDuration(83)
        self._ty_ani.setStartValue(self._translate_y)
        self._ty_ani.setEndValue(target)
        self._ty_ani.setEasingCurve(winui_easing())
        self._ty_ani.start()

    def _start_release_translate(self) -> None:
        self._ty_ani.stop()
        self._ty_ani.setDuration(167)
        self._ty_ani.setStartValue(self._translate_y)
        self._ty_ani.setEndValue(0.0)
        self._ty_ani.setEasingCurve(winui_easing())
        self._ty_ani.start()
