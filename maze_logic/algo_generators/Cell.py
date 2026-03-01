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