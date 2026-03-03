"""Kill-and-hunt maze generator implementation.

Provides :class:`KillHuntGenerator`, a concrete implementation of the
hunt-and-kill algorithm for generating mazes. This class derives from
:class:`BaseGenerator` and is typically instantiated through the
:class:`mazegen.MazeGenerator.MazeGenerator` facade rather than used
directly.
"""

import random as rand
import sys
from typing import Optional, Tuple
from .BaseGenerator import BaseGenerator


class KillHuntGenerator(BaseGenerator):
    """Concrete hunt-and-kill maze generator.

    The algorithm alternates between random walks (the *kill* phase)
    and scanning for unvisited cells adjacent to the carved maze (the
    *hunt* phase). Common generator behaviour is provided by
    :class:`BaseGenerator`.
    """

    def kill(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Perform a random-walk carving from ``pos`` until trapped.

        During this phase, the generator repeatedly picks a random valid
        direction and carves passages until no unvisited neighbours are
        available.

        Args:
            pos: Starting cell coordinates ``(row, col)`` for the walk.

        Returns:
            tuple[int, int]: The final position where the walk stopped.
        """
        dim = ["top", "bottom", "left", "right"]
        while True:
            tmp_roots = dim.copy()
            moved = False

            for _ in range(4):
                root = rand.choice(tmp_roots)
                tmp_roots.remove(root)

                if self.check_root(pos, root):
                    pos = self.walk(root, pos)
                    self.grid[pos[0]][pos[1]].visited = True
                    moved = True
                    break

            if not moved:
                return pos

    def hunt(self) -> Optional[Tuple[int, int]]:
        """Scan the grid for an unvisited cell adjacent to the maze.

        If such a cell is found, a connection is carved to a visited
        neighbour and the coordinates of that cell are returned so that
        a new kill phase can start from there.

        Returns:
            tuple[int, int] | None: Coordinates of the next starting
            cell, or ``None`` when the entire grid has been visited.
        """
        H = self.HEIGHT - 1
        W = self.WIDTH - 1

        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.grid[y][x].visited is False and not self.grid[y][x].blocked:  # noqa: E501
                    if (
                        y > 0
                        and self.grid[y - 1][x].visited is True
                        and not self.grid[y - 1][x].blocked
                    ):
                        self.grid[y][x].top = 0
                        self.grid[y - 1][x].bottom = 0
                        return (y, x)
                    if (
                        y < H
                        and self.grid[y + 1][x].visited is True
                        and not self.grid[y + 1][x].blocked
                    ):
                        self.grid[y][x].bottom = 0
                        self.grid[y + 1][x].top = 0
                        return (y, x)
                    if (
                        x < W
                        and self.grid[y][x + 1].visited is True
                        and not self.grid[y][x + 1].blocked
                    ):
                        self.grid[y][x].right = 0
                        self.grid[y][x + 1].left = 0
                        return (y, x)
                    if (
                        x > 0
                        and self.grid[y][x - 1].visited is True
                        and not self.grid[y][x - 1].blocked
                    ):
                        self.grid[y][x].left = 0
                        self.grid[y][x - 1].right = 0
                        return (y, x)
        return None

    def generate(self) -> None:
        """Generate a maze using the hunt-and-kill algorithm.

        This method resets the internal state, seeds the RNG, builds the
        grid, runs alternating kill/hunt phases until the maze is fully
        carved, and optionally applies the imperfect-maze post-process
        defined in :class:`BaseGenerator`.
        """
        if self.first_generation:
            self.walk_history = []
            rand.seed(self.seed)
            self.first_generation = False
        else:
            self.walk_history = []
            self.seed = rand.randint(-sys.maxsize, sys.maxsize)
            rand.seed(self.seed)
        self.grid = []
        self.generate_grid()
        self.add_42()
        H = self.HEIGHT - 1
        W = self.WIDTH - 1
        start: Optional[Tuple[int, int]]
        while True:
            start = (rand.randint(0, H), rand.randint(0, W))
            if not self.grid[start[0]][start[1]].blocked:
                break
        self.grid[start[0]][start[1]].visited = True
        while True:
            start = self.kill(start)
            start = self.hunt()
            self.update()
            if start is None:
                self.update()
                break
            self.grid[start[0]][start[1]].visited = True
        if self.perfect is False:
            self.make_inperfect()
