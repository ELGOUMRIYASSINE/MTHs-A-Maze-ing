import sys as args
import parse as parser
import random as rand

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
        object = [self.top, self.buttom, self.left, self.right]
        binary_str = ""
        for i in object:
            binary_str += str(object[i])
        return hex(int(binary_str, 2))[2].upper()


def update():
    with open("../maze_output.txt", "w") as f:
        for i in range(parser.config['HEIGHT']):
            if not i == 0:
                f.write("\n")
            for n in range(parser.config['WIDTH']):
                f.write(str(grid[i][n]))


def hunt(is_start):
    if is_start is True:
        x = rand.randint(0, parser.config['WIDTH'])
        y = rand.randint(0, parser.config['HEIGHT'])
        return [y, x]
    for y in range(parser.config['HEIGHT']):
        for x in range(parser.config['WIDTH']):
            if grid[y][x].visited is False:
                return [y, x]


def kill():
    dim = [1, 2, 3, 4]
    while True:
        state = hunt
        if not state:
            break

grid = []
for y in range(parser.config['HEIGHT']):
    row = []
    for x in range(parser.config['WIDTH']):
        cell = Cell(x, y)
        row.append(cell)
    grid.append(row)
        
        
        



update()
kill()