"""Cell representation used by maze generators.

This module defines the `Cell` class which stores wall information
and state flags for a single cell in the maze grid.
"""
# typing not required in this module


class Cell:
    """A single maze cell.

    Attributes:
        x (int): Column index.
        y (int): Row index.
        top (int): 1 if wall exists on top, 0 otherwise.
        bottom (int): 1 if wall exists on bottom, 0 otherwise.
        left (int): 1 if wall exists on left, 0 otherwise.
        right (int): 1 if wall exists on right, 0 otherwise.
        visited (bool): Whether the cell has been visited by generator.
        blocked (bool): Whether the cell is blocked (pattern drawing).
    """

    def __init__(
        self,
        x: int,
        y: int,
        top: int = 1,
        bottom: int = 1,
        left: int = 1,
        right: int = 1,
    ) -> None:
        self.top: int = top
        self.bottom: int = bottom
        self.left: int = left
        self.right: int = right
        self.x: int = x
        self.y: int = y
        self.visited: bool = False
        self.blocked: bool = False

    def __str__(self) -> str:
        """Return a compact hex representation of the cell walls.

        The wall bits are ordered as left, bottom, right, top then
        converted to a hexadecimal digit.
        """
        bits = [self.left, self.bottom, self.right, self.top]
        binary_str = "".join(str(b) for b in bits)
        return hex(int(binary_str, 2))[2].upper()
