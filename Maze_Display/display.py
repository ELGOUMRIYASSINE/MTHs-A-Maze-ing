
def render_maze():
    CHAR_V = "║"
    CHAR_H = "═"
    # Corners (For F=1111 looks)
    C_TL = "╔" # Top Left
    C_TR = "╗" # Top Right
    C_BL = "╚" # Bottom Left
    C_BR = "╝" # Bottom Right
    SPACE = " "
    string_hex = "FAF5FFF"
    maze_matrix = []

    for c in string_hex:
        val = int(c, 16)
        binary_string = format(val, '04b')
        bit_list = [int(bit) for bit in binary_string]
        maze_matrix.append(bit_list)
    i = 0
    j = 0
    for c in range(0, 4):
        for r in maze_matrix:
            if r[c - 1] == 1 and c == 1 and i == 0:
                print(C_TL, end="")
                print(CHAR_H * 6, end="")
                print(C_TR, end="")
            elif r[c - 1] == 0 and c == 1:
                print(SPACE * 8, end="");
            # if r[c - 1] == 1 and
            #     i += 1
    print(maze_matrix)

render_maze()
# print("╔══════╗")
# print("║      ║")
# print("║      ║")
# print("╚══════╝")
