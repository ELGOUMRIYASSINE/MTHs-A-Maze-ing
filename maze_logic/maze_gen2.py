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
    def __init__(self, maze_file="maze_output.txt"):
        self.validate_config()
        self.height = parser.config['HEIGHT']
        self.width = parser.config['WIDTH']
        self.maze_file = maze_file
        self.grid = []
    @staticmethod
    def validate_config():
        try:
            if len(args.argv) == 2:
                parser.parse_config(args.argv[1])
            else:
                parser.parse_config()
        except Exception as e:
            print(e)
            exit()

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

    def draw_maze(self):
        for row in range(self.height):
            run = []

            for col in range(self.width):
                run.append((row, col))

                at_top_row  = (row == 0)
                at_last_col = (col == self.width - 1)

                # l7alat li kaynin
                if at_top_row:
                    if not at_last_col:
                        self.connect_east(row, col)

                elif at_last_col:
                    chosen = random.choice(run)
                    self.connect_north(chosen[0], chosen[1])
                    run = []
                else:
                    go_east = random.randint(0, 1) == 0

                    if go_east:
                        self.connect_east(row, col)
                    else:
                        chosen = random.choice(run)
                        self.connect_north(chosen[0], chosen[1])
                        run = []

grid = Grid("maze_output_2.txt")
grid.generate_grid()
grid.draw_maze()
grid.update()
