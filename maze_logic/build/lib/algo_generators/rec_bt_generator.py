import random as rand
import sys
from .MazeGenerator import MazeGenerator

sys.setrecursionlimit(10000)
class RecBTGenerator(MazeGenerator):
    def kill(self, pos):
        self.grid[pos[0]][pos[1]].visited = True
        
        dim = ["top", "bottom", "left", "right"]
        tmp_roots = dim.copy()

        for _ in range(4):
            root = rand.choice(tmp_roots)
            tmp_roots.remove(root)

            if self.check_root(pos, root):
                new_cell = self.walk(root, pos)
                self.kill(new_cell)

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
        H = self.HEIGHT - 1
        W = self.WIDTH - 1

        # start = [rand.randint(0, H), rand.randint(0, W)]
        while True:
            # randint YG """ get random integer within range of numbers """ YG
            start = [rand.randint(0, H), rand.randint(0, W)]
            if not self.grid[start[0]][start[1]].blocked:
                break
        self.grid[start[0]][start[1]].visited = True
        self.kill(start)
        if self.perfect == False:
            self.make_inperfect()
        self.update()
