"""Base maze generator classes and shared utilities.

This module defines the MazeGenerator abstract base class and common
utilities used by maze generation algorithms.
"""

import random as rand
import math
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from .Cell import Cell


class MazeGenerator(ABC):
    """Abstract base class for maze generators.

    Each concrete generator creates a grid of cells and implements a
    specific maze generation algorithm.

    Attributes:
        grid: 2D list of Cell objects representing the maze.
        walk_history: List of walk steps used for animation or replay.
        HEIGHT: Maze height in number of cells.
        WIDTH: Maze width in number of cells.
        entry: Entry coordinates list as [x, y] or similar.
        exit: Exit coordinates list as [x, y] or similar.
        first_generation: True if no maze has been generated yet.
        seed: Random seed used for the random number generator.
        perfect: True if the maze is required to have no loops.
        output_file: Path of the file where the maze is written.
        will_draw: True if an optional pattern should be drawn.
        pattern: Pattern selector (for example 42 or 1337).
    """

    seed_tracker: int = 0

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the maze generator with configuration values.

        Args:
            config: Dictionary with configuration keys such as HEIGHT,
                WIDTH, ENTRY, EXIT, SEED, PERFECT, OUTPUT_FILE, and
                PATTERN.
        """
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
        """Generate a maze and populate the internal grid.

        Subclasses must implement this method. They should create all
        cells, carve passages, and call :meth:`update` when finished.
        """
        raise NotImplementedError()

    def get_grid(self) -> List[List[Cell]]:
        """Return the current grid of cells.

        Returns:
            A 2D list of Cell objects representing the maze.
        """
        return self.grid

    @abstractmethod
    def kill(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Run one step of the algorithm-specific walk/kill phase.

        This is usually used by backtracking or recursive algorithms to
        continue carving from a given position.

        Args:
            pos: Current cell position as (y, x).

        Returns:
            The new position reached by the walk as (y, x), or None if
            the algorithm does not return a position.
        """
        raise NotImplementedError()

    def update(self, path_string: Optional[str] = None) -> None:
        """Write the current maze state to the output file.

        The grid, entry, and exit cells are written. If ``path_string``
        is provided, it is appended at the end of the file.

        Args:
            path_string: Optional string describing a path through the
                maze to append after the grid.
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
        """Reload configuration values into this generator instance.

        Existing values such as size, seed, and pattern are updated
        from the given configuration.

        Args:
            config: Dictionary containing the new configuration values.
        """
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
        """Add a few random extra openings to make the maze imperfect.

        This method breaks some additional walls to introduce loops in
        a maze that would otherwise be perfect.
        """
        walls_to_break = int(self.HEIGHT * self.WIDTH * 0.03)

        i = 0
        # to avoid infinit loops if
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
        """Create a fresh grid of Cell objects with all walls intact.

        The existing grid is replaced by a new HEIGHT x WIDTH grid.
        """
        self.grid = []
        for y in range(self.HEIGHT):
            row: List[Cell] = []
            for x in range(self.WIDTH):
                cell = Cell(x, y)
                row.append(cell)
            self.grid.append(row)
        self.update()

    def check_root(self, pos: Tuple[int, int], root: str) -> bool:
        """Check if the neighbouring cell in a direction is available.

        A neighbour is available if it is inside the grid, not visited,
        and not blocked.

        Args:
            pos: Current cell position as (y, x).
            root: Direction to check; one of "top", "bottom",
                "left", or "right".

        Returns:
            True if the neighbour in the given direction can be used,
            otherwise False.
        """
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
        """Carve a passage from a position in a given direction.

        This removes the wall between the current cell and the
        neighbour in the requested direction, records the step in
        ``walk_history``, and returns the new position.

        Args:
            root: Direction to move; one of "top", "bottom",
                "left", or "right".
            pos: Current cell position as (y, x).

        Returns:
            The new cell position as a (y, x) tuple.

        Raises:
            ValueError: If an unknown direction is given.
        """
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
        """Return the recorded walk history.

        Returns:
            A list of walk steps if any have been recorded, otherwise
            None.
        """
        if self.walk_history:
            return self.walk_history
        return None

    def add_42(self) -> None:
        """Apply a decorative numeric pattern to the maze grid.

        The pattern is drawn by marking some cells as blocked. If the
        configured pattern is 1337, a larger pattern is used;
        otherwise the default 42 pattern is drawn. If the maze is too
        small, no pattern is drawn.
        """
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
