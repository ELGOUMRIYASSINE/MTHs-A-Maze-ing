import sys as args
import parse.py


class Cell:
    def __init__(self, top=1, buttom=1, left=1, right=1):
        self.top = top
        self.buttom = buttom
        self.left = left
        self.right = right
        self.visited = False

    def __str__(self):
        object = [self.top, self.buttom, self.left, self.right]
        binary_str = ""
        for i in object:
            binary_str += str(object[i])
        print(binary_str)
        return hex(int(binary_str, 2))[2].upper()

W = 14
H = 19

grid = []
for i in range(H):
    cell = Cell()
    # cell = {1, 2, 3, 4}
    grid.append([cell]*W)

with open("../maze_output.txt", "w") as f:
    for i in range(H):
        print(f"row number {i} \n")
        if not i == 0:
            f.write("\n")
        for n in range(W):
            # print(f"column number {n} ")
            f.write(str(grid[i][n]))
            # print(str(grid[i][n]))
            # f.write(str())

# for n in range(H):
#     for m in range(W):
#         print(grid[n][m].top)