import unicodedata
import time
import sys
import pygame
# ANSI Colors
RESET = "\033[0m"
WHITE_BG = "\033[47m"
BLACK_BG = "\033[40m"
BLUE_BG = "\033[44m"
RED_BG = "\033[41m"
GREEN_BG = "\033[42m"
YELLOW_BG = "\033[43m"
CYAN_BG = "\033[46m"
CHAR_WATER = f"{CYAN_BG} {RESET}"

THEMS = [
    # Classic
    {"wall": WHITE_BG, "solid": BLUE_BG, "space": BLACK_BG},
    # Matrix
    {"wall": GREEN_BG, "solid": WHITE_BG, "space": BLACK_BG},
    # Fire
    {"wall": RED_BG, "solid": WHITE_BG, "space": BLACK_BG},
]

CHAR = f"{WHITE_BG} {RESET}"
CHAR_SOLUTION = f"{CYAN_BG} {RESET}"
SPACE = " "
TOM = "🐱"   # Entry
JERRY = "🐭"  # Exit

def setup_solid_matrix(animation_data):
    max_row = max(step[0] for step in animation_data)
    max_col = max(step[1] for step in animation_data )

    width = max_col + 1
    height = max_row + 1

    return ([[[1,1,1,1] for _ in range(width)] for _ in range(height)])

def break_wall(grid, r, c, direction):
    if direction == 'l':
        grid[r][c][0] = 0
    elif direction == 'b':
        grid[r][c][1] = 0
    elif direction == 'r':
        grid[r][c][2] = 0
    elif direction == 't':
        grid[r][c][3] = 0

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

from collections import deque

def get_water_history(matrix, start_pos, exit_pos):
    """Runs BFS and returns the exact order cells were explored"""
    queue = deque([start_pos])
    visited = set([start_pos])
    history = []  # This is our video timeline!

    while queue:
        c, r = queue.popleft() # c is X (col), r is Y (row)
        history.append((c, r))

        if (c, r) == exit_pos:
            break

        west, south, east, north = matrix[r][c]

        # Check all 4 directions (0 means no wall)
        neighbors = []
        if not west: neighbors.append((c - 1, r))
        if not south: neighbors.append((c, r + 1))
        if not east: neighbors.append((c + 1, r))
        if not north: neighbors.append((c, r - 1))

        for nc, nr in neighbors:
            # Ensure we stay inside the grid
            if 0 <= nr < len(matrix) and 0 <= nc < len(matrix[0]):
                if (nc, nr) not in visited:
                    visited.add((nc, nr))
                    queue.append((nc, nr))

    return history

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

    # We keep this so the path touches the Cat!
    coords = [(x, y)]

    # Remove the [1::2] hack! Just read every letter normally.
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

def animate_water_search(matrix, meta, theme_idx=0):
    entry_pos = meta['entry']
    exit_pos = meta['exit']

    # 1. Get the timeline of the flood
    flood_history = get_water_history(matrix, entry_pos, exit_pos)

    theme = THEMS[theme_idx]
    wall_color = f'{theme["wall"]} {RESET}'
    solid_color = f'{theme["solid"]} {RESET}'
    space_color = f'{theme["space"]} {RESET}'

    current_water = set()

    for step in flood_history:
        current_water.add(step)

        sys.stdout.write("\033[H")
        out = ""

        for r_idx, row in enumerate(matrix):
            line_top = ""
            line_mid = ""
            for c_idx, cell in enumerate(row):
                west, south, east, north = cell

                is_water = (c_idx, r_idx) in current_water
                water_north = (c_idx, r_idx - 1) in current_water
                water_west = (c_idx - 1, r_idx) in current_water

                line_top += wall_color
                if is_water and water_north and not north:
                    line_top += CHAR_WATER * 3
                else:
                    line_top += wall_color * 3 if north else space_color * 3

                if is_water and water_west and not west:
                    line_mid += CHAR_WATER
                else:
                    line_mid += wall_color if west else space_color

                if (c_idx, r_idx) == entry_pos:
                    line_mid += _fit_cell(TOM)
                elif (c_idx, r_idx) == exit_pos:
                    line_mid += _fit_cell(JERRY)
                elif is_water:
                    line_mid += CHAR_WATER * 3
                else:
                    line_mid += space_color * 3

            line_top += f"{wall_color}\n"
            line_mid += f"{wall_color}\n"
            out += line_top + line_mid

        line_bot = ""
        last_row = matrix[-1]
        for cell in last_row:
            west, south, east, north = cell
            line_bot += wall_color
            line_bot += wall_color * 3 if south else space_color * 3
        line_bot += f"{wall_color}\n"
        out += line_bot

        sys.stdout.write(out)
        sys.stdout.flush()

        time.sleep(0.04)

def render_frame(matrix, theme_idx=0, show_path=False):
    # This stops the terminal from scroling
    sys.stdout.write("\033[H")

    theme = THEMS[theme_idx]
    wall_color = f"{theme['wall']} {RESET}"
    solid_color = f"{theme['solid']} {RESET}"
    space_color = f"{theme['space']} {RESET}"

    out = ""
    for r_idx, row in enumerate(matrix):
        line_top = ""
        line_mid = ""
        for c_idx, cell in enumerate(row):
            west, south, east, north = cell
            is_solid = (west and south and east and north)

            line_top += wall_color
            line_top += wall_color * 3 if north else space_color * 3
            line_mid += wall_color if west else space_color

            if is_solid:
                line_mid += solid_color * 3
            else:
                line_mid += space_color * 3

        line_top += f"{wall_color}\n"
        line_mid += f"{wall_color}\n"

        out += line_top + line_mid

    line_bot = ""
    last_row = matrix[-1]
    for cell in last_row:
        west, south, east, north = cell
        line_bot += wall_color
        line_bot += wall_color * 3 if south else space_color * 3
    line_bot += f"{wall_color}\n"
    out += line_bot

    sys.stdout.write(out)
    sys.stdout.flush()

def animate_maze_generation(animation_data):
    matrix = setup_solid_matrix(animation_data)

    sys.stdout.write("\033[2J")

    for step in animation_data:
        r, c, direction = step

        break_wall(matrix, r, c, direction)

        # Draw the updated matrix to the screen
        render_frame(matrix)

        time.sleep(0.0001)

def animate_tom_walking(matrix, meta, path_coords_list, theme_idx=0, animate_walk=False, sound=True):
    entry_pos = meta['entry']
    exit_pos = meta['exit']
    theme = THEMS[theme_idx]

    wall_color = f'{theme["wall"]} {RESET}'
    solid_color = f'{theme["solid"]} {RESET}'
    space_color = f'{theme["space"]} {RESET}'

    TRAIL_BG = "\033[42m"
    TRAIL_CENTER = f"{TRAIL_BG} • {RESET}"
    TRAIL_DOOR = f"{TRAIL_BG}   {RESET}"
    TRAIL_VERT = f"{TRAIL_BG} {RESET}"

    # If animate is OFF, we only want to draw ONE frame (the final state)
    frames_to_draw = path_coords_list if animate_walk else [entry_pos]

    for step_idx, current_pos in enumerate(frames_to_draw):
        sys.stdout.write("\033[H")
        out = ""

        # If animated, trail grows step-by-step. If static, show the whole trail!
        if animate_walk:
            current_trail = set(path_coords_list[:step_idx+1])
        else:
            current_trail = set(path_coords_list)

        for r_idx, row in enumerate(matrix):
            line_top = ""
            line_mid = ""
            for c_idx, cell in enumerate(row):
                west, south, east, north = cell
                is_solid = (west and south and east and north)

                is_path = (c_idx, r_idx) in current_trail
                path_north = (c_idx, r_idx - 1) in current_trail
                path_west = (c_idx - 1, r_idx) in current_trail

                line_top += wall_color
                if is_path and path_north and not north:
                    line_top += TRAIL_DOOR
                else:
                    line_top += wall_color * 3 if north else space_color * 3

                if is_path and path_west and not west:
                    line_mid += TRAIL_VERT
                else:
                    line_mid += wall_color if west else space_color

                # Draw Tom, Jerry, and Trail
                if (c_idx, r_idx) == current_pos:
                    line_mid += _fit_cell(TOM)
                elif (c_idx, r_idx) == exit_pos:
                    line_mid += _fit_cell(JERRY)
                elif (c_idx, r_idx) == entry_pos and not animate_walk:
                    line_mid += _fit_cell(TOM) # Keep Tom at the start if static
                elif is_path:
                    line_mid += TRAIL_CENTER
                elif is_solid:
                    line_mid += solid_color * 3
                else:
                    line_mid += space_color * 3

            line_top += f"{wall_color}\n"
            line_mid += f"{wall_color}\n"
            out += line_top + line_mid

        line_bot = ""
        last_row = matrix[-1]
        for cell in last_row:
            west, south, east, north = cell
            line_bot += wall_color
            line_bot += wall_color * 3 if south else space_color * 3
        line_bot += f"{wall_color}\n"
        out += line_bot

        sys.stdout.write(out)
        sys.stdout.flush()

        # Only pause if we are actually animating!
        if animate_walk:
            time.sleep(0.08)

    if animate_walk is True and len(path_coords_list) > 1 and sound:
        pygame.mixer.init()
        sound = pygame.mixer.Sound("sounds/meow.mp3")
        # Play the sound for exactly 3000 milliseconds (3 seconds), then auto-stop
        sound.play(maxtime=3000)

# Add animate_walk to render_maze's arguments!
def render_maze(config, show_path=False, animate_walk=False, theme_idx=0, path_coords=None, path_string=None, animation_data=None, sound=True):
    matrix, meta = parse_maze_output(config['OUTPUT_FILE'])
    if not matrix:
        return

    if animation_data:
        animate_maze_generation(animation_data)
        time.sleep(0.5)
        sys.stdout.write("\033[H")
        sys.stdout.flush()

    entry_pos = meta['entry']

    if show_path and path_string:
        path_coords_list = get_path_coords(entry_pos[0], entry_pos[1], path_string)
    else:
        path_coords_list = [entry_pos]

    # Pass the new flag to the drawing function
    animate_tom_walking(matrix, meta, path_coords_list, theme_idx, animate_walk, sound)
    print()
