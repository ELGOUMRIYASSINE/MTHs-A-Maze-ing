import random
import parse as parser
import sys as args


class Cell:
    def __init__(self, x, y, top=1, bottom=1, left=1, right=1):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.x = x
        self.y = y

    def __str__(self):
        bits = [self.left, self.bottom, self.right, self.top]
        binary_str = "".join(str(b) for b in bits)
        return hex(int(binary_str, 2))[2].upper()


class Grid:
    def __init__(self, height, width, maze_file="maze_output.txt"):
        self.height = height
        self.width = width
        self.maze_file = maze_file
        self.grid = []

    def generate_grid(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell(x, y)
                row.append(cell)
            self.grid.append(row)
        self.update()

    def update(self):
        with open(self.maze_file, "w") as f:
            for i in range(self.height):
                if i != 0:
                    f.write("\n")
                for n in range(self.width):
                    f.write(str(self.grid[i][n]))
    def connect_east(self, row, col):
        self.grid[row][col].right = 0
        self.grid[row][col + 1].left = 0

    def connect_north(self, row, col):
        self.grid[row][col].top = 0
        self.grid[row - 1][col].bottom = 0


try:
    if len(args.argv) == 2:
        parser.parse_config(args.argv[1])
    else:
        parser.parse_config()
except Exception as e:
    print(e)
    exit()

grid = Grid(parser.config['HEIGHT'], parser.config['WIDTH'], "maze_output_2.txt")
grid.generate_grid()
