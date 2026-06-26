"""Fluent 2 typography ramp — 8 levels from caption to display."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from PyQt6.QtGui import QFont


class FontWeight(Enum):
    THIN = 100
    LIGHT = 300
    SEMI_LIGHT = 350
    REGULAR = 400
    SEMI_BOLD = 600
    BOLD = 700


@dataclass
class TypeRamp:
    size: int = 14
    weight: FontWeight = FontWeight.REGULAR


@dataclass
class Typography:
    fontFamily: str = "Segoe UI Variable"
    fallbackFamilies: list[str] = field(default_factory=lambda: ["Segoe UI", "Microsoft YaHei", "PingFang SC"])

    # Fluent 2 ramp: caption → body → bodyStrong → bodyLarge → subtitle → title → titleLarge → display
    caption: TypeRamp = field(default_factory=lambda: TypeRamp(12, FontWeight.REGULAR))
    body: TypeRamp = field(default_factory=lambda: TypeRamp(14, FontWeight.REGULAR))
    bodyStrong: TypeRamp = field(default_factory=lambda: TypeRamp(14, FontWeight.SEMI_BOLD))
    bodyLarge: TypeRamp = field(default_factory=lambda: TypeRamp(16, FontWeight.REGULAR))
    subtitle: TypeRamp = field(default_factory=lambda: TypeRamp(20, FontWeight.SEMI_BOLD))
    title: TypeRamp = field(default_factory=lambda: TypeRamp(24, FontWeight.SEMI_BOLD))
    titleLarge: TypeRamp = field(default_factory=lambda: TypeRamp(32, FontWeight.SEMI_BOLD))
    display: TypeRamp = field(default_factory=lambda: TypeRamp(48, FontWeight.SEMI_BOLD))

    def font(self, size: int = 14, weight: FontWeight = FontWeight.REGULAR) -> QFont:
        families = [self.fontFamily, *self.fallbackFamilies]
        return QFont(",".join(families), size, weight.value)

    def body_font(self) -> QFont:
        return self.font(self.body.size, self.body.weight)

    def title_font(self) -> QFont:
        return self.font(self.title.size, self.title.weight)
