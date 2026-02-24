import parse as parser
import random as rand
import math


class Cell:
    def __init__(self, x, y, top=1, bottom=1, left=1, right=1):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.x = x
        self.y = y
        self.visited = False
        self.blocked = False

    def __str__(self):
        bits = [self.left, self.bottom, self.right, self.top]
        binary_str = "".join(str(b) for b in bits)
        return hex(int(binary_str, 2))[2].upper()


class MazeGenerator:
    def __init__(self, config):
        self.grid = []
        self.HEIGHT = config['HEIGHT']
        self.WIDTH = config['WIDTH']
        self.entry = config['ENTRY']
        self.exit = config['EXIT']
        self.output_file = config['OUTPUT_FILE']

    def update(self, final=True):
        with open(self.output_file, "w") as f:
            for i in range(parser.config['HEIGHT']):
                if not i == 0:
                    f.write("\n")
                for n in range(parser.config['WIDTH']):
                    f.write(str(self.grid[i][n]))
            if final:
                f.write("\n\n")
                f.write(",".join(str(nbr) for nbr in self.entry))
                f.write("\n")
                f.write(",".join(str(nbr) for nbr in self.exit))
                f.write("\n")
                f.write("SWSESWSESWSSSEESEEENEESESEESSSEEESSSEEENNENEE")

    def generate_grid(self):
        for y in range(parser.config['HEIGHT']):
            row = []
            for x in range(parser.config['WIDTH']):
                cell = Cell(x, y)
                row.append(cell)
            self.grid.append(row)
        self.update()

    def check_root(self, pos, root):
        y, x = pos
        if root == "top":
            return (
                y > 0
                and not self.grid[y - 1][x].visited
                and not self.grid[y - 1][x].blocked
            )
        if root == "bottom":
            return (
                y < parser.config["HEIGHT"] - 1
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
                x < parser.config["WIDTH"] - 1
                and not self.grid[y][x + 1].visited
                and not self.grid[y][x + 1].blocked
            )
        return False

    def walk(self, root, pos):
        y, x = pos
        if root == "top":
            self.grid[y][x].top = 0
            self.grid[y - 1][x].bottom = 0
            return [y - 1, x]
        if root == "bottom":
            self.grid[y][x].bottom = 0
            self.grid[y + 1][x].top = 0
            return [y + 1, x]
        if root == "right":
            self.grid[y][x].right = 0
            self.grid[y][x + 1].left = 0
            return [y, x + 1]
        if root == "left":
            self.grid[y][x].left = 0
            self.grid[y][x - 1].right = 0
            return [y, x - 1]

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

    def add_42(self):
        area_h, area_w = 5, 7
        start_y = math.floor((parser.config['HEIGHT'] - area_h) / 2)
        start_x = math.floor((parser.config['WIDTH'] - area_w) / 2)

        pattern = [
            [1, 0, 1, 0, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1]
        ]

        for p_y in range(area_h):
            for p_x in range(area_w):
                if pattern[p_y][p_x] == 1:
                    self.grid[start_y + p_y][start_x + p_x].blocked = True

    def generate(self):
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
                self.update(True)
                break
            self.grid[start[0]][start[1]].visited = True
