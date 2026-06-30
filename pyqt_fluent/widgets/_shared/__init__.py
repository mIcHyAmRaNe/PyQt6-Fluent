"""Shared widget primitives — reusable paint helpers and base classes.

Every widget category (buttons, inputs, navigation, etc.) uses these
instead of reimplementing focus rings, ripples, shadows, or icon rendering.
"""

from .background_animation import BackgroundAnimationWidget  # noqa: F401
from .focus_ring import FocusRing  # noqa: F401
from .icon_widget import IconWidget  # noqa: F401
from .ripple import RippleEffect  # noqa: F401
from .shadow import DropShadow  # noqa: F401
from .theme_aware import ThemeAwareWidget  # noqa: F401
from .translate_animation import TranslateYAnimation  # noqa: F401
