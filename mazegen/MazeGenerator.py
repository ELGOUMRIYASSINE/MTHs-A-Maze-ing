"""Base maze generator classes and shared utilities.

This module provides the abstract `MazeGenerator` base class used by
concrete maze generation implementations in this package.
"""

import random as rand
import math
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from .Cell import Cell


class MazeGenerator(ABC):
    """Abstract base class for maze generators.

    Subclasses must implement `generate` and `kill`. The class stores the
    generated grid and configuration used by the algorithms.
    """

    seed_tracker: int = 0

    def __init__(self, config: Dict[str, Any]) -> None:
        self.__class__.seed_tracker += 1
        self.grid: List[List[Cell]] = []
        self.walk_history: List[List[Any]] = []
        self.HEIGHT: int = int(config["HEIGHT"])
        self.WIDTH: int = int(config["WIDTH"])
        self.entry: List[int] = config.get("ENTRY", [])
        self.exit: List[int] = config.get("EXIT", [])
        self.first_generation: bool = True
        if "SEED" in config:
            self.seed: int = int(config.get("SEED", 0))
        else:
            self.seed = rand.randint(0, 1000000)
        self.perfect: bool = bool(config.get("PERFECT", True))
        self.output_file: str = str(config.get("OUTPUT_FILE", "maze_output.txt"))  # noqa: E501
        self.will_draw: bool = True
        if config.get("PATTERN"):
            self.pattern: int = int(config["PATTERN"])
        else:
            self.pattern = 42

    @abstractmethod
    def generate(self) -> None:
        """Run the maze generation algorithm and populate `self.grid`.

        Concrete implementations should write the final maze into
        `self.grid` and call `self.update()` when finished.
        """
        raise NotImplementedError()

    def get_grid(self) -> List[List[Cell]]:
        """Return the current grid of cells."""
        return self.grid

    @abstractmethod
    def kill(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Generator-specific walk/kill operation starting at `pos`.

        Subclasses implement how they traverse / carve the maze from
        the provided starting position. Implementations may return the
        final position reached (as a `(y, x)` tuple) or `None` when no
        such value is applicable.
        """
        raise NotImplementedError()

    def update(self, path_string: Optional[str] = None) -> None:
        """Write the current maze state to `self.output_file`.

        If `path_string` is provided, append it to the output.
        """
        if not self.grid:
            return
        with open(self.output_file, "w") as f:
            for i in range(self.HEIGHT):
                if i != 0:
                    f.write("\n")
                for n in range(self.WIDTH):
                    f.write(str(self.grid[i][n]))
            f.write("\n\n")
            f.write(",".join(str(nbr) for nbr in self.entry))
            f.write("\n")
            f.write(",".join(str(nbr) for nbr in self.exit))
            f.write("\n")
            if path_string:
                f.write(path_string)

    def reload_config(self, config: Dict[str, Any]) -> None:
        """Reload configuration values into this generator instance."""
        self.HEIGHT = int(config["HEIGHT"])
        self.WIDTH = int(config["WIDTH"])
        self.entry = config.get("ENTRY", [])
        self.exit = config.get("EXIT", [])
        self.first_generation = True
        self.seed = int(config.get("SEED", self.seed))
        self.perfect = bool(config.get("PERFECT", self.perfect))
        self.output_file = str(config.get("OUTPUT_FILE", self.output_file))
        if config.get("PATTERN"):
            self.pattern = int(config["PATTERN"])
        else:
            self.pattern = 42

    def make_inperfect(self) -> None:
        walls_to_break = int(self.HEIGHT * self.WIDTH * 0.03)

        i = 0
        iterations = 0

        dim = ["top", "bottom", "left", "right"]

        while i < walls_to_break and iterations < 1000:
            iterations += 1

            y = rand.randint(1, self.HEIGHT - 2)
            x = rand.randint(1, self.WIDTH - 2)

            tmp_roots = dim.copy()
            rand.shuffle(tmp_roots)

            if self.grid[y][x].blocked:
                continue

            for root in tmp_roots:
                if root == "top":
                    if not self.grid[y - 1][x].blocked:
                        if self.grid[y][x].top == 1:
                            self.grid[y][x].top = 0
                            self.grid[y - 1][x].bottom = 0
                            i += 1
                            break

                if root == "bottom":
                    if not self.grid[y + 1][x].blocked:
                        if self.grid[y][x].bottom == 1:
                            self.grid[y][x].bottom = 0
                            self.grid[y + 1][x].top = 0
                            i += 1
                            break

                if root == "left":
                    if not self.grid[y][x - 1].blocked:
                        if self.grid[y][x].left == 1:
                            self.grid[y][x].left = 0
                            self.grid[y][x - 1].right = 0
                            i += 1
                            break

                if root == "right":
                    if not self.grid[y][x + 1].blocked:
                        if self.grid[y][x].right == 1:
                            self.grid[y][x].right = 0
                            self.grid[y][x + 1].left = 0
                            i += 1
                            break
        self.update()

    def generate_grid(self) -> None:
        """Create a fresh grid of `Cell` objects with all walls intact."""
        for y in range(self.HEIGHT):
            row: List[Cell] = []
            for x in range(self.WIDTH):
                cell = Cell(x, y)
                row.append(cell)
            self.grid.append(row)
        self.update()

    def check_root(self, pos: Tuple[int, int], root: str) -> bool:
        """Return True if the neighbour in `root` direction is available."""
        y, x = pos
        if root == "top":
            return (
                y > 0
                and not self.grid[y - 1][x].visited
                and not self.grid[y - 1][x].blocked
            )
        if root == "bottom":
            return (
                y < self.HEIGHT - 1
                and not self.grid[y + 1][x].visited
                and not self.grid[y + 1][x].blocked
            )
        if root == "left":
            return (
                x > 0
                and not self.grid[y][x - 1].visited
                and not self.grid[y][x - 1].blocked
            )
        if root == "right":
            return (
                x < self.WIDTH - 1
                and not self.grid[y][x + 1].visited
                and not self.grid[y][x + 1].blocked
            )
        return False

    def walk(self, root: str, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Carve passage in direction `root` from `pos` and return new pos."""
        y, x = pos
        next_pos: Tuple[int, int]
        if root == "top":
            self.grid[y][x].top = 0
            self.grid[y - 1][x].bottom = 0
            self.walk_history.append([y, x, "t"])
            self.walk_history.append([y - 1, x, "b"])
            next_pos = (y - 1, x)
        elif root == "bottom":
            self.grid[y][x].bottom = 0
            self.grid[y + 1][x].top = 0
            self.walk_history.append([y, x, "b"])
            self.walk_history.append([y + 1, x, "t"])
            next_pos = (y + 1, x)
        elif root == "right":
            self.grid[y][x].right = 0
            self.grid[y][x + 1].left = 0
            self.walk_history.append([y, x, "r"])
            self.walk_history.append([y, x + 1, "l"])
            next_pos = (y, x + 1)
        elif root == "left":
            self.grid[y][x].left = 0
            self.grid[y][x - 1].right = 0
            self.walk_history.append([y, x, "l"])
            self.walk_history.append([y, x - 1, "r"])
            next_pos = (y, x - 1)
        else:
            raise ValueError(f"Unknown root direction: {root}")

        return next_pos

    def get_walk_history(self) -> Optional[List[List[Any]]]:
        """Return the recorded walk history if present."""
        if self.walk_history:
            return self.walk_history
        return None

    def add_42(self) -> None:
        self.will_draw = True
        pattern_42 = [
            [1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]

        pattern_1337 = [
            [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],  # noqa: E501
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],  # noqa: E501
            [0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0],  # noqa: E501
            [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],  # noqa: E501
            [0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0],  # noqa: E501
            [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],  # noqa: E501
        ]

        pattern = pattern_42
        if self.pattern == 1337:
            pattern = pattern_1337
        else:
            self.pattern = 42

        if not (self.WIDTH > len(pattern[0]) + 1 and self.HEIGHT > len(pattern) + 1):  # noqa: E501
            self.will_draw = False
            return
        area_h, area_w = len(pattern), len(pattern[0])
        start_y = math.floor((self.HEIGHT - area_h) / 2)
        start_x = math.floor((self.WIDTH - area_w) / 2)

        for p_y in range(area_h):
            for p_x in range(area_w):
                if pattern[p_y][p_x] == 1:
                    self.grid[start_y + p_y][start_x + p_x].blocked = True
