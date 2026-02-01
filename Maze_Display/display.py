import time

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

        top_wall = CHAR_H * CELL_WIDTH if north else SPACE * CELL_WIDTH
        line_top += f"{C_TL}{top_wall}{C_TR}"
        # West Wall Logic
        w_wall = CHAR_V if west else SPACE

        # East Wall Logic
        e_wall = CHAR_V if east else SPACE

        # The empty space in the center
        inner_space = SPACE * CELL_WIDTH

        # Glue: Left Wall + Space + Right Wall
        line_mid1 += f"{w_wall}{inner_space}{e_wall}"
        line_mid2 += f"{w_wall}{inner_space}{e_wall}"
    # print(maze_matrix)
        # If south bit is 1, use "══════", otherwise use "      "
        bot_wall = CHAR_H * CELL_WIDTH if south else SPACE * CELL_WIDTH

        # Glue: Corner + Wall + Corner
        line_bot += f"{C_BL}{bot_wall}{C_BR}"

    def type_writer(text, speed=0.01):
        for char in text:
            print(char, end="") # flush=True forces immediate printing
            time.sleep(speed)
        print() # Move to next line after loop finishes

    # --- 4. PRINT WITH ANIMATION ---
    print("\nRendering Maze...\n")

    type_writer(line_top)
    type_writer(line_mid1)
    type_writer(line_mid2)
    type_writer(line_bot)
render_maze()

