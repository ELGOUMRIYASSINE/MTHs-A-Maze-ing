import sys as args
import parse as parser
import random as rand
import math


grid = []
try:
    if len(args.argv) == 2:
        parser.parse_config(args.argv[1])
    else:
        parser.parse_config()
except Exception as e:
    print(e)
    exit()


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


def update():
    with open("../maze_output.txt", "w") as f:
        for i in range(parser.config['HEIGHT']):
            if not i == 0:
                f.write("\n")
            for n in range(parser.config['WIDTH']):
                f.write(str(grid[i][n]))


def generate_grid():
    for y in range(parser.config['HEIGHT']):
        row = []
        for x in range(parser.config['WIDTH']):
            cell = Cell(x, y)
            row.append(cell)
        grid.append(row)
    update()


def check_root(pos, root):
    y, x = pos
    if root == "top":
        return (
            y > 0
            and not grid[y - 1][x].visited
            and not grid[y - 1][x].blocked
        )
    if root == "bottom":
        return (
            y < parser.config["HEIGHT"] - 1
            and not grid[y + 1][x].visited
            and not grid[y + 1][x].blocked
        )
    if root == "left":
        return (
            x > 0
            and not grid[y][x - 1].visited
            and not grid[y][x - 1].blocked
        )
    if root == "right":
        return (
            x < parser.config["WIDTH"] - 1
            and not grid[y][x + 1].visited
            and not grid[y][x + 1].blocked
        )
    return False


def walk(root, pos):
    y, x = pos
    if root == "top":
        grid[y][x].top = 0
        grid[y - 1][x].bottom = 0
        return [y - 1, x]
    if root == "bottom":
        grid[y][x].bottom = 0
        grid[y + 1][x].top = 0
        return [y + 1, x]
    if root == "right":
        grid[y][x].right = 0
        grid[y][x + 1].left = 0
        return [y, x + 1]
    if root == "left":
        grid[y][x].left = 0
        grid[y][x - 1].right = 0
        return [y, x - 1]


def kill(pos):
    dim = ["top", "bottom", "left", "right"]
    while True:
        tmp_roots = dim.copy()
        moved = False

        for _ in range(4):
            root = rand.choice(tmp_roots)
            tmp_roots.remove(root)

            if check_root(pos, root):
                pos = walk(root, pos)
                grid[pos[0]][pos[1]].visited = True
                moved = True
                break

        if not moved:
            return pos


def hunt():
    H = parser.config['HEIGHT'] - 1
    W = parser.config['WIDTH'] - 1

    for y in range(parser.config['HEIGHT']):
        for x in range(parser.config['WIDTH']):
            if grid[y][x].visited is False and not grid[y][x].blocked:
                if y > 0 and grid[y - 1][x].visited is True and not grid[y - 1][x].blocked:
                    grid[y][x].top = 0
                    grid[y - 1][x].bottom = 0
                    return [y, x]
                if y < H and grid[y + 1][x].visited is True and not grid[y + 1][x].blocked:
                    grid[y][x].bottom = 0
                    grid[y + 1][x].top = 0
                    return [y, x]
                if x < W and grid[y][x + 1].visited is True and not grid[y][x + 1].blocked:
                    grid[y][x].right = 0
                    grid[y][x + 1].left = 0
                    return [y, x]
                if x > 0 and grid[y][x - 1].visited is True and not grid[y][x - 1].blocked:
                    grid[y][x].left = 0
                    grid[y][x - 1].right = 0
                    return [y, x]
    return None


def add_42():
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
                grid[start_y + p_y][start_x + p_x].blocked = True

if __name__ == "__main__":
    generate_grid()
    add_42()
    H = parser.config['HEIGHT'] - 1
    W = parser.config['WIDTH'] - 1

    start = [rand.randint(0, H), rand.randint(0, W)]
    full = False
    grid[start[0]][start[1]].visited = True
    while True:
        start = kill(start)
        grid[start[0]][start[1]].visited = True
        start = hunt()
        update()
        if start is None:
            break
        grid[start[0]][start[1]].visited = True