"""Resolves token paths through the 3-tier system."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PyQt6.QtGui import QColor

from .component import ComponentTokens, ControlState
from .palette import Palette
from .semantic import SemanticPalette


@dataclass
class TokenResolver:
    palette: Palette
    semantic: SemanticPalette
    component: ComponentTokens
    is_dark: bool = False

    def resolve(self, path: str) -> Any:
        if path.startswith("component."):
            key = path[10:]
            parts = key.split(".", 1)
            ref = getattr(self.component, parts[0])
            if len(parts) > 1:
                state = parts[1]
                if isinstance(ref, ControlState):
                    return self.resolve(getattr(ref, state))
                return ref
            if isinstance(ref, ControlState):
                return self.resolve(ref.rest)
            if isinstance(ref, str):
                return self.resolve(ref)
            return ref

        if path.startswith("semantic."):
            key = path[9:]
            ref = self.semantic.ref(key, self.is_dark)
            return self.resolve(ref)

        if path.startswith("palette."):
            key = path[8:]
            return self.palette.resolve(key, self.is_dark)

        return self.palette.resolve(path, self.is_dark)

    def color(self, path: str) -> QColor:
        val = self.resolve(path)
        if isinstance(val, QColor):
            return val
        raise TypeError(f"Token {path} resolved to {type(val).__name__}, expected QColor")

    def int(self, path: str) -> int:
        val = self.resolve(path)
        if isinstance(val, int):
            return val
        raise TypeError(f"Token {path} resolved to {type(val).__name__}, expected int")

    def str(self, path: str) -> str:
        val = self.resolve(path)
        if isinstance(val, str):
            return val
        raise TypeError(f"Token {path} resolved to {type(val).__name__}, expected str")
