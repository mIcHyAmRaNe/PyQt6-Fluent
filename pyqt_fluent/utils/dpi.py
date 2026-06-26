"""DPI scaling utilities for custom painting and native events.

Qt automatically scales most things (QSS, geometries, fonts) based on the
logical DPI. However, two cases require manual scaling:

1. Custom paintEvent: Coordinates and dimensions computed manually (e.g., shadows, acrylic effects).
2. Native events (Win32): `WM_NCHITTEST` and other native messages use physical pixels.

This module provides helpers for these cases.
"""

from __future__ import annotations

from PyQt6.QtCore import QPoint, QRect, QSize
from PyQt6.QtGui import QGuiApplication


class DpiHelper:
    """Helper class for DPI-aware scaling."""

    @staticmethod
    def screen_scale_factor(screen=None) -> float:
        """Return the device pixel ratio for the specified screen.

        If no screen is provided, the primary screen is used.

        Returns:
            float: The scale factor (e.g., 1.0 for 96 DPI, 1.5 for 144 DPI, 2.0 for 192 DPI).
        """
        if screen is None:
            screen = QGuiApplication.primaryScreen()
        return screen.devicePixelRatio()

    @staticmethod
    def logical_to_physical(value: int | float, screen=None) -> float:
        """Scale a logical value (e.g., from QRect) to physical pixels.

        Args:
            value: The logical value to scale.
            screen: Optional screen. Uses primary screen if not provided.

        Returns:
            float: The value in physical pixels.
        """
        return value * DpiHelper.screen_scale_factor(screen)

    @staticmethod
    def physical_to_logical(value: int | float, screen=None) -> float:
        """Scale a physical pixel value to logical pixels.

        Args:
            value: The physical pixel value to scale.
            screen: Optional screen. Uses primary screen if not provided.

        Returns:
            float: The value in logical pixels.
        """
        return value / DpiHelper.screen_scale_factor(screen)

    @staticmethod
    def scale_point(point: QPoint, screen=None) -> QPoint:
        """Scale a QPoint from logical to physical pixels.

        Args:
            point: The point in logical coordinates.
            screen: Optional screen. Uses primary screen if not provided.

        Returns:
            QPoint: The point in physical pixels.
        """
        scale = DpiHelper.screen_scale_factor(screen)
        return QPoint(int(point.x() * scale), int(point.y() * scale))

    @staticmethod
    def scale_rect(rect: QRect, screen=None) -> QRect:
        """Scale a QRect from logical to physical pixels.

        Args:
            rect: The rectangle in logical coordinates.
            screen: Optional screen. Uses primary screen if not provided.

        Returns:
            QRect: The rectangle in physical pixels.
        """
        scale = DpiHelper.screen_scale_factor(screen)
        return QRect(
            int(rect.x() * scale),
            int(rect.y() * scale),
            int(rect.width() * scale),
            int(rect.height() * scale),
        )

    @staticmethod
    def scale_size(size: QSize, screen=None) -> QSize:
        """Scale a QSize from logical to physical pixels.

        Args:
            size: The size in logical coordinates.
            screen: Optional screen. Uses primary screen if not provided.

        Returns:
            QSize: The size in physical pixels.
        """
        scale = DpiHelper.screen_scale_factor(screen)
        return QSize(int(size.width() * scale), int(size.height() * scale))

    @staticmethod
    def unscale_point(point: QPoint, screen=None) -> QPoint:
        """Scale a QPoint from physical to logical pixels.

        Args:
            point: The point in physical pixels.
            screen: Optional screen. Uses primary screen if not provided.

        Returns:
            QPoint: The point in logical coordinates.
        """
        scale = DpiHelper.screen_scale_factor(screen)
        return QPoint(int(point.x() / scale), int(point.y() / scale))

    @staticmethod
    def unscale_rect(rect: QRect, screen=None) -> QRect:
        """Scale a QRect from physical to logical pixels.

        Args:
            rect: The rectangle in physical pixels.
            screen: Optional screen. Uses primary screen if not provided.

        Returns:
            QRect: The rectangle in logical coordinates.
        """
        scale = DpiHelper.screen_scale_factor(screen)
        return QRect(
            int(rect.x() / scale),
            int(rect.y() / scale),
            int(rect.width() / scale),
            int(rect.height() / scale),
        )
