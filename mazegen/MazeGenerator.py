"""High-level maze generator factory.

This module exposes the :class:`MazeGenerator` facade which builds
algorithm-specific generator instances (e.g. recursive backtracking and
hunt-and-kill) from a common configuration dictionary.
"""

from typing import Any

from .BaseGenerator import BaseGenerator
from .kill_hunt_generator import KillHuntGenerator
from .rec_bt_generator import RecBTGenerator


class MazeGenerator:
    """Maze generator facade.

    This class provides a unified interface for creating maze generator
    instances using different algorithms, such as recursive backtracking
    and hunt-and-kill. Each generator is configured via a common
    settings dictionary.
    """

    def kill_hunt_gen(self, config: dict[str, Any]) -> BaseGenerator:
        """Create a hunt-and-kill maze generator.

        The returned instance is a concrete subclass of
        :class:`BaseGenerator` configured from the provided ``config``
        dictionary.

        Args:
            config (dict): Parsed configuration containing maze settings
                such as dimensions, output file, seed, pattern, and
                whether the maze should be perfect or imperfect.

        Returns:
            BaseGenerator: A generator that uses the hunt-and-kill
            algorithm.
        """
        return KillHuntGenerator(config)

    def rec_bt_generator(self, config: dict[str, Any]) -> BaseGenerator:
        """Create a recursive-backtracking maze generator.

        The returned instance is a concrete subclass of
        :class:`BaseGenerator` configured from the provided ``config``
        dictionary.

        Args:
            config (dict): Parsed configuration containing maze settings
                such as dimensions, output file, seed, pattern, and
                whether the maze should be perfect or imperfect.

        Returns:
            BaseGenerator: A generator that uses the recursive
            backtracking algorithm.
        """
        return RecBTGenerator(config)
