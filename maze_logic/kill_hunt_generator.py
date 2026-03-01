import parse as parser
import random as rand
from .MazeGenerator import MazeGenerator
import sys

class KillHuntGenerator(MazeGenerator):
    def kill(self, pos):
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

    def hunt(self):
        H = parser.config['HEIGHT'] - 1
        W = parser.config['WIDTH'] - 1

        for y in range(parser.config['HEIGHT']):
            for x in range(parser.config['WIDTH']):
                if self.grid[y][x].visited is False and not self.grid[y][x].blocked:
                    if y > 0 and self.grid[y - 1][x].visited is True and not self.grid[y - 1][x].blocked:
                        self.grid[y][x].top = 0
                        self.grid[y - 1][x].bottom = 0
                        return [y, x]
                    if y < H and self.grid[y + 1][x].visited is True and not self.grid[y + 1][x].blocked:
                        self.grid[y][x].bottom = 0
                        self.grid[y + 1][x].top = 0
                        return [y, x]
                    if x < W and self.grid[y][x + 1].visited is True and not self.grid[y][x + 1].blocked:
                        self.grid[y][x].right = 0
                        self.grid[y][x + 1].left = 0
                        return [y, x]
                    if x > 0 and self.grid[y][x - 1].visited is True and not self.grid[y][x - 1].blocked:
                        self.grid[y][x].left = 0
                        self.grid[y][x - 1].right = 0
                        return [y, x]
        return None

    def generate(self):
        if self.first_generation:
            rand.seed(self.seed)
            self.first_generation = False
        else:
            self.seed = rand.randint(-sys.maxsize, sys.maxsize)
            rand.seed(self.seed)
        self.grid = []
        self.generate_grid()
        self.add_42()
        H = parser.config['HEIGHT'] - 1
        W = parser.config['WIDTH'] - 1
        # pick a number that is not in 42
        while True:
            # randint YG """ get random integer within range of numbers """ YG
            start = [rand.randint(0, H), rand.randint(0, W)]
            if not self.grid[start[0]][start[1]].blocked:
                break
        self.grid[start[0]][start[1]].visited = True
        while True:
            start = self.kill(start)
            self.grid[start[0]][start[1]].visited = True
            start = self.hunt()
            self.update()
            if start is None:
                self.update()
                break
            self.grid[start[0]][start[1]].visited = True
        if self.perfect == False:
            self.make_inperfect()
