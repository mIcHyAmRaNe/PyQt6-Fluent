"""Shared widget primitives — reusable paint helpers and base classes.

Every widget category (buttons, inputs, navigation, etc.) uses these
instead of reimplementing focus rings, ripples, shadows, or icon rendering.
"""

from .focus_ring import FocusRing  # noqa: F401
from .ripple import RippleEffect  # noqa: F401
from .shadow import DropShadow  # noqa: F401
from .icon_widget import IconWidget  # noqa: F401
