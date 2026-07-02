"""Theme-aware SVG icon widget — delegates to the centralized icon system."""

from __future__ import annotations

from ...icons.widget import IconWidget as _CentralizedIconWidget


class IconWidget(_CentralizedIconWidget):
    """Backward-compatible alias — use ``pyqt_fluent.icons.IconWidget`` directly."""

    def __init__(self, icon_path: str = "", color_ref: str = "semantic.control_fg",
                 fill_ref: str = "", parent=None):
        # Extract icon name from path if provided
        icon_name = ""
        if icon_path:
            import os
            icon_name = os.path.splitext(os.path.basename(icon_path))[0]
        super().__init__(
            icon_name=icon_name,
            color_ref=color_ref,
            fill_ref=fill_ref,
            parent=parent,
        )
