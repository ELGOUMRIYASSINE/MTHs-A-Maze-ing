import unicodedata


# ANSI Colors
RESET = "\033[0m"
WHITE_BG = "\033[47m"
BLACK_BG = "\033[40m"
BLUE_BG = "\033[43m"
RED_BG = "\033[41m"
GREEN_BG = "\033[42m"
YELLOW_BG = "\033[43m"

THEMS = [
    # Classic
    {"wall": WHITE_BG, "solid": BLUE_BG, "space": BLACK_BG},
    # Matrix
    {"wall": GREEN_BG, "solid": WHITE_BG, "space": BLACK_BG},
    # Fire
    {"wall": RED_BG, "solid": WHITE_BG, "space": BLACK_BG},
]

CHAR = f"{WHITE_BG} {RESET}"
CHAR_SOLUTION = f"{GREEN_BG} {RESET}"
SPACE = " "
TOM = "🐱"   # Entry
JERRY = "🐭"  # Exit


def _display_width(text: str) -> int:
    width = 0
    for ch in text:
        if unicodedata.combining(ch):
            continue
        width += 2 if unicodedata.east_asian_width(ch) in {"W", "F"} else 1
    return width


def _fit_cell(text: str, cell_width: int = 3) -> str:
    """
    Make sure the returned string occupies exactly `cell_width` terminal
    columns. This avoids visual shifting when using wide glyphs (e.g. emojis).
    """
    w = _display_width(text)
    if w == cell_width:
        return text
    if w < cell_width:
        return text + (SPACE * (cell_width - w))
    return " ? "[:cell_width]


def parse_maze_output(filename):
    matrix = []
    meta = {}
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            i = 0

            while i < len(lines) and lines[i]:
                row = []
                for c in lines[i]:
                    value = int(c, 16)
                    value = format(value, "04b")
                    bits = [int(x) for x in value]
                    row.append(bits)
                matrix.append(row)
                i += 1

            while i < len(lines) and not lines[i]:
                i += 1

            if i + 1 < len(lines):
                meta['entry'] = tuple(map(int, lines[i].split(',')))
                meta['exit'] = tuple(map(int, lines[i + 1].split(',')))

    except FileNotFoundError:
        print("Error: File not found")
        return [], {}
    return matrix, meta


def get_path_coords(entry_x, entry_y, path_string):
    x, y = entry_x, entry_y
    coords = []

    for ch in path_string.strip():
        if ch == "N":
            y -= 1
        elif ch == "S":
            y += 1
        elif ch == "E":
            x += 1
        elif ch == "W":
            x -= 1
        else:
            continue
        coords.append((x, y))

    return coords


def render_maze(config, show_path=False, theme_idx=0, path_coords=None, path_string=None):
    matrix, meta = parse_maze_output(config['OUTPUT_FILE'])
    if not matrix:
        return
    entry_pos = meta['entry']
    exit_pos = meta['exit']
    path_coords = set()
    if show_path and path_string:
        path_coords = set(
            get_path_coords(entry_pos[0], entry_pos[1], path_string),
        )
    theme = THEMS[theme_idx]
    wall_color = f'{theme["wall"]} {RESET}'
    solid_color = f'{theme["solid"]} {RESET}'
    space_color = f'{theme["space"]} {RESET}'

    for r_idx, row in enumerate(matrix):
        line_top = ""
        line_mid = ""
        for c_idx, cell in enumerate(row):
            west, south, east, north = cell
            is_solid = (west and south and east and north)
            
            is_path = show_path and (c_idx, r_idx) in path_coords
            path_north = show_path and (c_idx, r_idx - 1) in path_coords
            path_west = show_path and (c_idx - 1, r_idx) in path_coords

            line_top += wall_color
            if is_path and path_north and not north:
                line_top += CHAR_SOLUTION * 3 
            else:
                line_top += wall_color * 3 if north else space_color * 3

            if is_path and path_west and not west:
                line_mid += CHAR_SOLUTION 
            else:
                line_mid += wall_color if west else space_color

            if (c_idx, r_idx) == entry_pos:
                line_mid += _fit_cell(TOM)
            elif (c_idx, r_idx) == exit_pos:
                line_mid += _fit_cell(JERRY)
            elif is_solid:
                line_mid += solid_color * 3
            elif is_path:
                line_mid += CHAR_SOLUTION * 3
            else:
                line_mid += space_color * 3
    
        line_top += wall_color
        line_mid += wall_color

        print(line_top)
        print(line_mid)

    line_bot = ""
    last_row = matrix[-1]
    for cell in last_row:
        west, south, east, north = cell
        line_bot += wall_color
        line_bot += wall_color * 3 if south else space_color * 3
    line_bot += wall_color
    print(line_bot)
    print()
