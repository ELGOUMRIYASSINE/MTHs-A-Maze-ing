import os
import unicodedata


# ANSI Colors
RESET = "\033[0m"
WHITE_BG = "\033[47m"
BLACK_BG = "\033[40m"
BLUE_BG = "\033[44m"
RED_BG = "\033[41m"
GREEN_BG = "\033[42m"
YELLOW_BG = "\033[43m"

THEMS = [
    #Classic
    {"wall": WHITE_BG, "solid": BLUE_BG, "space": BLACK_BG},
    #Matrix
    {"wall": GREEN_BG, "solid": WHITE_BG, "space": BLACK_BG},
    #Fire
    {"wall": RED_BG, "solid": WHITE_BG, "space": BLACK_BG}
]

CHAR = f"{WHITE_BG} {RESET}"
# CHAR = "█"
SPACE = " "
TOM = "🐱"  # Entry
JERRY = "🐭" # Exit
def _display_width(text: str) -> int:
    width = 0
    for ch in text:
        # Combining marks have zero width
        if unicodedata.combining(ch):
            continue
        # East Asian Wide/Fullwidth usually take 2 columns in terminals (many emojis too)
        width += 2 if unicodedata.east_asian_width(ch) in {"W", "F"} else 1
    return width


def _fit_cell(text: str, cell_width: int = 3) -> str:
    """
    Make sure the returned string occupies exactly `cell_width` terminal columns.
    This avoids visual shifting when using wide glyphs (e.g. emojis).
    """
    w = _display_width(text)
    if w == cell_width:
        return text
    if w < cell_width:
        return text + (SPACE * (cell_width - w))
    # Too wide: fallback to a single ASCII marker
    return " ? "[:cell_width]

def parse_maze_output(filename):
    matrix = []
    meta = {}
    try:
        with open(filename, 'r') as file:
            lines = [l.strip() for l in file.readlines()]
            i = 0

            # Parse Maze grids
            while i < len(lines) and lines[i]:
                row = []
                for c in lines[i]:
                    value = int(c, 16)
                    value = format(value, "04b")
                    bits = [int(x) for x in value]
                    row.append(bits)
                matrix.append(row)
                i += 1

            # Skip potential empty lines
            while i < len(lines) and not lines[i]:
                i += 1

            # Parse metadata
            if i + 2 < len(lines):
                # Convert coords to integers immediately here for safety
                meta['entry'] = tuple(map(int, lines[i].split(',')))
                meta['exit'] = tuple(map(int, lines[i+1].split(',')))
                meta['path'] = lines[i+2]

    except FileNotFoundError:
        print("Error: File not found")
        return [], {}
    return matrix, meta

def get_path_coords(entry_x, entry_y, path_string):
    pass

def render_maze(config, show_path=False, theme_idx=0):
    matrix, meta = parse_maze_output(config['OUTPUT_FILE']) # Use local file
    if not matrix: return
    entry_pos = meta['entry']
    exit_pos = meta['exit']
    theme = THEMS[theme_idx]
    # TODO: You still need to convert meta['path'] string to a list of (x,y) coordinates
    # path_coords = conv ert_path_to_coords(entry_pos, meta['path'])
    # wall_char = f"{WHITE_BG} {RESET}"
    WALL = f'{theme["wall"]} {RESET}'
    SOLID = f'{theme["solid"]} {RESET}'
    SPACE = f'{theme["space"]} {RESET}'

    for r_idx, row in enumerate(matrix):
        line_top = ""
        line_mid = ""
        for c_idx, cell in enumerate(row):
            west, south, east, north = cell
            is_solid = (west and south and east and north)

            # 1. TOP LINE
            line_top += WALL
            line_top += WALL * 3 if north else SPACE * 3

            # 2. MID LINE (The Fix: Mutually Exclusive Checks)
            line_mid += WALL if west else SPACE

            # Check what goes in the center (Priority Order)
            if (c_idx, r_idx) == entry_pos:
                line_mid += _fit_cell(TOM)  # Draw entry (fits 3 columns)
            elif (c_idx, r_idx) == exit_pos:
                line_mid += _fit_cell(JERRY)  # Draw exit (fits 3 columns)
            elif is_solid:
                line_mid += SOLID * 3    # Draw Wall Block
            # elif show_path and (c_idx, r_idx) in path_coords:
            #     line_mid += " * "     # Draw Path Dot
            else:
                line_mid += SPACE * 3   # Draw Empty Space

        # Close the row
        line_top += WALL
        line_mid += WALL

        print(line_top)
        print(line_mid)

    # Bottom Line of the maze
    line_bot = ""
    last_row = matrix[-1]
    for cell in last_row:
        west, south, east, north = cell
        line_bot += WALL
        line_bot += WALL * 3 if south else SPACE * 3
    line_bot += WALL
    print(line_bot)
    print()
