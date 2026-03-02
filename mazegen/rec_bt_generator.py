"""Recursive backtracking maze generator implementation.

This module provides `RecBTGenerator`, a recursive backtracking
algorithm implementation subclassing `MazeGenerator`.
"""

import random as rand
import sys
from typing import List, Tuple
from .MazeGenerator import MazeGenerator

sys.setrecursionlimit(10000)


class RecBTGenerator(MazeGenerator):
    """Recursive backtracking generator.

    The algorithm marks cells as visited and recursively visits available
    neighbours chosen at random.
    """

    def kill(self, pos: Tuple[int, int]) -> None:
        """Recursively visit and carve passages starting from `pos`."""
        self.grid[pos[0]][pos[1]].visited = True

        dim = ["top", "bottom", "left", "right"]
        tmp_roots: List[str] = dim.copy()

        for _ in range(4):
            root = rand.choice(tmp_roots)
            tmp_roots.remove(root)

            if self.check_root(pos, root):
                new_cell = self.walk(root, pos)
                self.kill(new_cell)

    def generate(self) -> None:
        """Generate a maze using recursive backtracking."""
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

        while True:
            start = [rand.randint(0, H), rand.randint(0, W)]
            if not self.grid[start[0]][start[1]].blocked:
                break
        self.grid[start[0]][start[1]].visited = True
        # start is a list [y,x] but kill expects Tuple[int,int] semantics
        self.kill((start[0], start[1]))
        if self.perfect is False:
            self.make_inperfect()
        self.update()
