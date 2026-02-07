import sys as args
import time
import parse as parser
import random as rand

# args.path.append('../Maze_Display')
# import display


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
        object = [self.top, self.right, self.buttom, self.left]
        binary_str = ""
        for i in object:
            binary_str += str(i)
        return hex(int(binary_str, 2))[2].upper()


def update(grid):
    with open("../maze_output.txt", "w") as f:
        for i in range(parser.config['HEIGHT']):
            if not i == 0:
                f.write("\n")
            for n in range(parser.config['WIDTH']):
                f.write(str(grid[i][n]))


def generate_grid():
    grid = []
    for y in range(parser.config['HEIGHT']):
        row = []
        for x in range(parser.config['WIDTH']):
            cell = Cell(x, y)
            row.append(cell)
        grid.append(row)
    update(grid)
    return grid

def check_root(grid, pos, root):
    y, x = pos
    if root == "top":
        if y > 0 and grid[y][x].top == 1 and grid[y - 1][x].visited is False:
            return True
    if root == "bottom":
        if y < parser.config["HEIGHT"] and grid[y][x].bottom == 1 and grid[y + 1][x].visited is False:
            return True
    if root == "left":
        if x > 0 and grid[y][x].left == 1 and grid[y][x - 1].visited is False:
            return True
    if root == "right":
        if x < parser.config["WIDTH"] and grid[y][x].right == 1 and grid[y][x + 1].visited is False:
            return True
    return False


def walk(grid, root, pos):
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


def kill(grid, pos):
    dim = ["top", "buttom", "left", "right"]
    while True:
        tmp_roots = dim.copy()
        time_to_hunt = True
        for i in range(4):
            root = rand.choice(tmp_roots)
            if check_root(grid[pos[0]][pos[1]], root) is True:
                time_to_hunt = False
                pos = walk(grid, root, pos)
                update(grid)
                grid[pos[0]][pos[1]].visited = True
        if time_to_hunt is True:
            raise ValueError


def hunt(grid):
    H = parser.config['HEIGHT'] - 1
    W = parser.config['WIDTH'] - 1

    for y in range(H):
        for x in range(W):
            if grid[y][x].visited is False:
                if y > 0 and grid[y - 1][x].visited is True:
                    grid[y][x].top = 0
                    grid[y - 1][x].bottom = 0
                    return [y, x]
                if y < H and grid[y + 1][x].visited is True:
                    grid[y][x].bottom = 0
                    grid[y + 1][x].top = 0
                    return [y, x]
                if x < W and grid[y][x + 1].visited is True:
                    grid[y][x].right = 0
                    grid[y][x + 1].left = 0
                    return [y, x]
                if x > 0 and grid[y][x - 1].visited is True:
                    grid[y][x].left = 0
                    grid[y][x - 1].right = 0
                    return [y, x]
    return None 


if __name__ == "__main__":
    # generate the initial grid
    grid = generate_grid()

    H = parser.config['HEIGHT'] - 1
    W = parser.config['WIDTH'] - 1

    start = [rand.randint(0, H), rand.randint(0, W)]
    full = False
    grid[start[0]][start[1]].visited = True
    while full is False:
        print("jj")
        try:
            kill(grid, start)
        except Exception:
            start = hunt(grid)
            update(grid)
        if start is None:
            full = True

