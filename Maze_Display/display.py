"""Render and animate maze states in the terminal.

This module parses maze output files and provides rendering and animation
helpers for maze generation, solving, and path display.
"""

from collections import deque
from collections.abc import Mapping, Sequence
from typing import Any
import unicodedata
import time
import sys
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


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

Cell = list[int]
MazeMatrix = list[list[Cell]]
Position = tuple[int, int]
Meta = dict[str, Position]
AnimationStep = tuple[int, int, str]

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


def setup_solid_matrix(animation_data: Sequence[AnimationStep]) -> MazeMatrix:
    """Create a fully walled matrix sized from animation data.

    Args:
        animation_data: Sequence of animation steps as (row, col, direction).

    Returns:
        A maze matrix initialized with all walls set.
    """
    max_row = max(step[0] for step in animation_data)
    max_col = max(step[1] for step in animation_data)

    width = max_col + 1
    height = max_row + 1

    return [[[1, 1, 1, 1] for _ in range(width)] for _ in range(height)]


def break_wall(grid: MazeMatrix, r: int, c: int, direction: str) -> None:
    """Open one wall of a cell based on a direction code.

    Args:
        grid: Maze matrix to update.
        r: Row index of the target cell.
        c: Column index of the target cell.
        direction: Wall code ('l', 'b', 'r', or 't').
    """
    if direction == 'l':
        grid[r][c][0] = 0
    elif direction == 'b':
        grid[r][c][1] = 0
    elif direction == 'r':
        grid[r][c][2] = 0
    elif direction == 't':
        grid[r][c][3] = 0


def _display_width(text: str) -> int:
    """Return terminal display width for a text string.

    Args:
        text: Text to measure.

    Returns:
        The number of terminal columns used by the text.
    """
    width = 0
    for ch in text:
        if unicodedata.combining(ch):
            continue
        width += 2 if unicodedata.east_asian_width(ch) in {"W", "F"} else 1
    return width


def _fit_cell(text: str, cell_width: int = 3) -> str:
    """Fit text to an exact terminal cell width.

    Args:
        text: Text to place in a cell.
        cell_width: Target terminal width in columns.

    Returns:
        A string that occupies exactly ``cell_width`` columns.
    """
    w = _display_width(text)
    if w == cell_width:
        return text
    if w < cell_width:
        return text + (SPACE * (cell_width - w))
    return " ? "[:cell_width]


def get_water_history(
    matrix: MazeMatrix,
    start_pos: Position,
    exit_pos: Position,
) -> list[Position]:
    """Run BFS and return visited cells in exploration order.

    Args:
        matrix: Maze matrix with wall definitions.
        start_pos: Start position as (x, y).
        exit_pos: Exit position as (x, y).

    Returns:
        List of visited positions in the order they were explored.
    """
    queue = deque([start_pos])
    visited = set([start_pos])
    history = []  # This is our video timeline!

    while queue:
        c, r = queue.popleft()  # c is X (col), r is Y (row)
        history.append((c, r))

        if (c, r) == exit_pos:
            break

        west, south, east, north = matrix[r][c]

        # Check all 4 directions (0 means no wall)
        neighbors = []
        if not west:
            neighbors.append((c - 1, r))
        if not south:
            neighbors.append((c, r + 1))
        if not east:
            neighbors.append((c + 1, r))
        if not north:
            neighbors.append((c, r - 1))

        for nc, nr in neighbors:
            # Ensure we stay inside the grid
            if 0 <= nr < len(matrix) and 0 <= nc < len(matrix[0]):
                if (nc, nr) not in visited:
                    visited.add((nc, nr))
                    queue.append((nc, nr))

    return history


def parse_maze_output(filename: str) -> tuple[MazeMatrix, Meta]:
    """Parse a maze output file into matrix data and metadata.

    Args:
        filename: Path to the maze output file.

    Returns:
        A tuple of (matrix, meta). ``meta`` may contain ``entry`` and ``exit``.
    """
    matrix: MazeMatrix = []
    meta: Meta = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file]
            if len(lines) < 2:
                raise ValueError("The output file corrupted, can't display anything Thank you !")  # noqa: E501
            i = 0

            while i < len(lines) and lines[i]:
                row = []
                for c in lines[i]:
                    int_value = int(c, 16)
                    bit_string = format(int_value, "04b")
                    bits = [int(x) for x in bit_string]
                    row.append(bits)
                matrix.append(row)
                i += 1

            while i < len(lines) and not lines[i]:
                i += 1

            if i + 1 < len(lines):
                raw_entry = tuple(map(int, lines[i].split(',')))
                raw_exit = tuple(map(int, lines[i + 1].split(',')))
                if len(raw_entry) == 2 and len(raw_exit) == 2:
                    meta['entry'] = (raw_entry[0], raw_entry[1])
                    meta['exit'] = (raw_exit[0], raw_exit[1])

    except FileNotFoundError:
        print("Error: File not found")
        return [], {}
    except ValueError as e:
        print(e)
        exit()
    return matrix, meta


def get_path_coords(
    entry_x: int,
    entry_y: int,
    path_string: str,
) -> list[Position]:
    """Convert a path string into grid coordinates.

    Args:
        entry_x: Entry x-coordinate.
        entry_y: Entry y-coordinate.
        path_string: Path using N/S/E/W directions.

    Returns:
        Ordered list of path positions including the entry.
    """
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


def animate_water_search(
    matrix: MazeMatrix,
    meta: Meta,
    theme_idx: int = 0,
) -> None:
    """Animate BFS flood exploration from entry to exit.

    Args:
        matrix: Maze matrix to animate.
        meta: Maze metadata containing entry and exit positions.
        theme_idx: Theme index for rendering colors.
    """
    entry_pos = meta['entry']
    exit_pos = meta['exit']

    # 1. Get the timeline of the flood
    flood_history = get_water_history(matrix, entry_pos, exit_pos)

    theme = THEMS[theme_idx]
    wall_color = f'{theme["wall"]} {RESET}'
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


def render_frame(
    matrix: MazeMatrix,
    theme_idx: int = 0,
    show_path: bool = False,
) -> None:
    """Render one maze frame to the terminal.

    Args:
        matrix: Maze matrix to render.
        theme_idx: Theme index for rendering colors.
        show_path: Unused flag kept for compatibility.
    """
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


def animate_maze_generation(
    animation_data: Sequence[AnimationStep],
    config: Mapping[str, Any],
) -> None:
    """Animate maze carving steps in the terminal.

    Args:
        animation_data: Sequence of wall-break animation steps.
        config: Maze configuration used to compute animation speed.
    """
    matrix = setup_solid_matrix(animation_data)

    sys.stdout.write("\033[2J")

    for step in animation_data:
        r, c, direction = step

        break_wall(matrix, r, c, direction)

        # Draw the updated matrix to the screen
        render_frame(matrix)
        speed = float(((config['HEIGHT'] * config['WIDTH']) * 0.02) / 625)
        time.sleep(speed)


def animate_tom_walking(
    matrix: MazeMatrix,
    meta: Meta,
    path_coords_list: Sequence[Position],
    theme_idx: int = 0,
    animate_walk: bool = False,
    sound: bool = True,
    config: Mapping[str, Any] | None = None,
) -> None:
    """Render Tom moving along the solved path.

    Args:
        matrix: Maze matrix to render.
        meta: Maze metadata containing entry and exit positions.
        path_coords_list: Ordered path coordinates to display.
        theme_idx: Theme index for rendering colors.
        animate_walk: If True, animate step-by-step movement.
        sound: If True, play end sound when animation completes.
        config: Optional config mapping (currently unused).
    """
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

        # If animated, trail grows step-by-step.
        # If static, show the whole trail.
        if animate_walk:
            current_trail = set(path_coords_list[:step_idx + 1])
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
                    # Keep Tom at the start if static.
                    line_mid += _fit_cell(TOM)
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
        import pygame

        pygame.mixer.init()
        meow_sound = pygame.mixer.Sound("sounds/meow.mp3")
        # Play sound for exactly 3000 milliseconds (3 seconds), then auto-stop
        meow_sound.set_volume(1.0)
        meow_sound.play(maxtime=3000)


# Add animate_walk to render_maze's arguments!
def render_maze(
    config: Mapping[str, Any],
    show_path: bool = False,
    animate_walk: bool = False,
    theme_idx: int = 0,
    path_coords: Sequence[Position] | None = None,
    path_string: str | None = None,
    animation_data: Sequence[AnimationStep] | None = None,
    sound: bool = True,
) -> None:
    """Render the maze, optional generation animation, and solution path.

    Args:
        config: Maze configuration containing output file path.
        show_path: If True, display the solution path.
        animate_walk: If True, animate Tom walking the solution path.
        theme_idx: Theme index for rendering colors.
        path_coords: Optional precomputed path coordinates.
        path_string: Optional path string using N/S/E/W directions.
        animation_data: Optional generation steps for carve animation.
        sound: If True, play sound effects when applicable.
    """
    matrix, meta = parse_maze_output(config['OUTPUT_FILE'])
    if not matrix:
        return

    if animation_data:
        animate_maze_generation(animation_data, config)
        time.sleep(0.5)
        sys.stdout.write("\033[H")
        sys.stdout.flush()

    entry_pos = meta['entry']
    exit_pos = meta['exit']

    path_coords_list = [entry_pos]
    if show_path and path_coords:
        candidate_path = list(path_coords)
        candidate_is_grid_path = (
            bool(candidate_path)
            and candidate_path[0] == entry_pos
            and candidate_path[-1] == exit_pos
            and all(
                0 <= x < len(matrix[0]) and 0 <= y < len(matrix)
                for x, y in candidate_path
            )
        )
        if candidate_is_grid_path:
            path_coords_list = candidate_path
        elif path_string:
            path_coords_list = get_path_coords(
                entry_pos[0],
                entry_pos[1],
                path_string,
            )
    elif show_path and path_string:
        path_coords_list = get_path_coords(
            entry_pos[0],
            entry_pos[1],
            path_string,
        )

    # Pass the new flag to the drawing function
    animate_tom_walking(
        matrix,
        meta,
        path_coords_list,
        theme_idx,
        animate_walk,
        sound,
        config,
    )
    print()
