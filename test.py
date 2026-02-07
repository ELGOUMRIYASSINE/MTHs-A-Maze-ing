import sys as args
import time
import parse as parser
import random as rand
args.path.append('../Maze_Display')
import display


try:
    if len(args.argv) == 2:
        parser.parse_config(args.argv[1])
    else:
        parser.parse_config()
except Exception as e:
    print(e)
    exit()


class Cell:
    def __init__(self, x, y, top=1, buttom=1, left=1, right=1):
        self.top = top
        self.buttom = buttom
        self.left = left
        self.right = right
        self.x = x
        self.y = y
        self.visited = False

    def __str__(self):
        # Renderer expects: west, south, east, north (1 = wall)
        bits = [self.left, self.buttom, self.right, self.top]
        binary_str = "".join(str(b) for b in bits)
        return hex(int(binary_str, 2))[2].upper()


def update(grid):
    with open("../maze_output.txt", "w") as f:
        for i in range(parser.config['HEIGHT']):
            if not i == 0:
                f.write("\n")
            for n in range(parser.config['WIDTH']):
                f.write(str(grid[i][n]))


def hunt(is_start=False):
    if is_start is True:
        x = rand.randint(0, parser.config['WIDTH'] - 1)
        y = rand.randint(0, parser.config['HEIGHT'] - 1)
        return [y, x]
    for y in range(parser.config['HEIGHT']):
        for x in range(parser.config['WIDTH']):
            if grid[y][x].visited is False:
                if y > 0:
                    if grid[y - 1][x].visited is True:
                        # grid[y][x].top = 0
                        # grid[y-1][x].buttom = 0
                        return [y, x]
                if  y + 1 <= parser.config['HEIGHT'] - 1:
                    if grid[y + 1][x].visited is True:
                        # grid[y][x].buttom = 0
                        # grid[y+1][x].top = 0
                        return [y, x]
                if  x - 1 >= 0:
                    if grid[y][x - 1].visited is True:
                        # grid[y][x - 1].right = 0
                        # grid[y][x].left = 0
                        return [y, x]
                if  x + 1 <= parser.config['WIDTH'] - 1:
                    if grid[y][x + 1].visited is True:
                        # grid[y][x + 1].left = 0
                        # grid[y][x].right = 0
                        return [y, x]
    return None


def change_state(cell, root):
    W = parser.config['WIDTH']
    H = parser.config['HEIGHT']

    y = cell.y
    x = cell.x

    if root == "top":
        if y - 1 < 0:
            return None
        grid[y][x].top = 0
        grid[y - 1][x].buttom = 0
        return [y - 1, x]

    if root == "buttom":
        if y + 1 > H - 1:
            return None
        grid[y][x].buttom = 0
        grid[y + 1][x].top = 0
        return [y + 1, x]

    if root == "right":
        if x + 1 > W - 1:
            return None
        grid[y][x].right = 0
        grid[y][x + 1].left = 0
        return [y, x + 1]

    if root == "left":
        if x - 1 < 0:
            return None
        grid[y][x].left = 0
        grid[y][x - 1].right = 0
        return [y, x - 1]

    return None

grid = []
for y in range(parser.config['HEIGHT']):
    row = []
    for x in range(parser.config['WIDTH']):
        cell = Cell(x, y)
        row.append(cell)
    grid.append(row)
update(grid)


def check_root(cell, root):
    if root == "right":
        if cell.x + 1 > parser.config['WIDTH'] - 1:
            return False
        if grid[cell.y][cell.x + 1].visited is False and grid[cell.y][cell.x - 1].right == 1:
            return True
    if root == "left":
        if cell.x - 1 < 0:
            return False
        if grid[cell.y][cell.x - 1].visited is False and grid[cell.y][cell.x - 1].left == 1:
            return True
    if root == "top":
        if cell.y - 1 < 0:
            return False
        if grid[cell.y - 1][cell.x].visited is False and  grid[cell.y][cell.x - 1].top == 1:
            return True

    if root == "buttom":
        if cell.y + 1 > parser.config['HEIGHT'] - 1:
            return False
        if grid[cell.y + 1][cell.x].visited is False and  grid[cell.y][cell.x - 1].buttom == 1:
            return True
    return False



def kill():
    dim = ["top", "buttom", "left", "right"]
    r = hunt(True)
    counter = 0
    while True:
        if r is None:
            break
        grid[r[0]][r[1]].visited = True
        tmp_roots = dim.copy()
        a = False
        for i in range(4):
            root = rand.choice(tmp_roots)
            if check_root(grid[r[0]][r[1]], root) is True:
                a = True
                break
            else:
                tmp_roots.remove(root)
        if a is False:
            counter += 1
            r = hunt(False)
        else:
            r = change_state(grid[r[0]][r[1]], root)
        update(grid)
        # print(counter)



kill()
