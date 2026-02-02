import time

def render_maze(string_hex = "FAF5FFF"):
    CHAR_V = "║"
    CHAR_H = "═"
    # Corners (For F=1111 looks)
    C_TL = "╔" # Top Left
    C_TR = "╗" # Top Right
    C_BL = "╚" # Bottom Left
    C_BR = "╝" # Bottom Right
    SPACE = " "
    maze_matrix = []

    line_top = ""
    line_mid1 = ""
    line_mid2 = ""
    line_bot = ""
    CELL_WIDTH = 6

    for c in string_hex:
        val = int(c, 16)
        binary_string = format(val, '04b')
        bit_list = [int(bit) for bit in binary_string]
        maze_matrix.append(bit_list)
    for bits in maze_matrix:
        west, south, east, north = bits
        middle_part = CHAR_H * 6 if north else SPACE * CELL_WIDTH
        line_top += f"{C_TL}{middle_part}{C_TR}"

        line_mid1 += f"{CHAR_V}{SPACE * 6}" if west else f"{SPACE * 7}"
        line_mid1 += f"{CHAR_V}" if east else f"{SPACE}"

        line_mid2 += f"{CHAR_V}{SPACE * 6}" if west else f"{SPACE * 7}"
        line_mid2 += f"{CHAR_V}" if east else f"{SPACE}"

        middle_part = CHAR_H * 6 if south else SPACE * CELL_WIDTH
        line_bot += f"{C_BL}{middle_part}{C_BR}"
    print(line_top)
    print(line_mid1)
    print(line_mid2)
    print(line_bot)

def maze_parser():
    try:
        with open("../maze_output.txt", 'r') as file:
            line = file.readline()
            while line:
                render_maze(line.strip())
                line = file.readline()
    except FileNotFoundError:
        print("File: 'maze_output.txt' not found !")
maze_parser()
