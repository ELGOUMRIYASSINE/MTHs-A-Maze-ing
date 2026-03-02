"""Configuration parsing and maze output parsing utilities.

This module provides helpers to parse the project's `config.txt` and
to read maze files produced by the generators.
"""

import math
from typing import Any, Dict, List, Tuple, NoReturn

# Type aliases
Matrix = List[List[List[int]]]
Meta = Dict[str, Any]


config_keys: List[str] = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
]
# Module-level configuration dictionary populated by `parse_config()`.
config: Dict[str, Any] = {}


def config_error(message: str) -> NoReturn:
    """Raise a configuration `ValueError` with `message`."""
    raise ValueError(message)


def check_path() -> None:
    """Validate `ENTRY`/`EXIT` positions and pattern placement.

    Uses and may update the module-level `config` mapping.
    """
    width: int = config["WIDTH"]
    height: int = config["HEIGHT"]

    if "PATTERN" not in config:
        config["PATTERN"] = 42

    x, y = config["ENTRY"]
    x2, y2 = config["EXIT"]

    # ENTRY and EXIT cannot be the same
    if x == x2 and y == y2:
        config_error("ENTRY and EXIT cannot be the same position.")

    # ENTRY inside maze boundaries
    if not (0 <= x < width and 0 <= y < height):
        config_error("ENTRY position is outside the maze boundaries.")

    # EXIT inside maze boundaries
    if not (0 <= x2 < width and 0 <= y2 < height):
        config_error("EXIT position is outside the maze boundaries.")

    # Patterns
    pattern_42 = [
        [1, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1],
    ]

    pattern_1337 = [
        [0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    ]

    pattern = pattern_42
    if config['PATTERN'] == 1337:
        pattern = pattern_1337

    area_h = len(pattern)
    area_w = len(pattern[0])

    if not (width > area_w + 1 and height > area_h + 1):
        return

    start_y = math.floor((height - area_h) / 2)
    start_x = math.floor((width - area_w) / 2)

    for p_y in range(area_h):
        for p_x in range(area_w):
            if pattern[p_y][p_x] == 0:
                continue
            if start_y + p_y == y and start_x + p_x == x:
                config_error("ENTRY cannot be placed inside the pattern area.")
            if start_y + p_y == y2 and start_x + p_x == x2:
                config_error("EXIT cannot be placed inside the pattern area.")


def value_valid(key: str, value: str) -> None:
    """Validate and normalize a single configuration `key`/`value` pair.

    On success the normalized value is stored in the module-level
    `config` mapping.
    """
    if key.islower():
        key = key.upper()

    if key in ("WIDTH", "HEIGHT"):
        try:
            ivalue = int(value)
        except ValueError:
            config_error(f"{key} must be a valid integer number.")

        if key == "WIDTH" and not (3 <= ivalue <= 55):
            config_error("WIDTH must be between 3 and 55.")

        if key == "HEIGHT" and not (3 <= ivalue <= 55):
            config_error("HEIGHT must be between 3 and 55.")

        config[key] = ivalue

    elif key in ("ENTRY", "EXIT"):
        parts = value.split(",")
        if len(parts) != 2:
            config_error(f"{key} must be in format: x,y (example: 3,5)")

        try:
            config[key] = (int(parts[0]), int(parts[1]))
        except ValueError:
            config_error(f"{key} coordinates must be integers.")

    elif key == "OUTPUT_FILE":
        if not value:
            config_error("OUTPUT_FILE is missing or empty.")

        try:
            with open(value, "w"):
                pass
        except PermissionError:
            config_error(
                "Cannot write to OUTPUT_FILE. Please check permissions."
            )
        except IsADirectoryError:
            config_error("OUTPUT_FILE cannot be a directory.")
        except Exception:
            config_error("Unexpected error while processing OUTPUT_FILE.")

        config[key] = value

    elif key == "PERFECT":
        if value == "True":
            config[key] = True
        elif value == "False":
            config[key] = False
        else:
            config_error("PERFECT must be either True or False.")

    elif key == "SEED":
        try:
            config[key] = int(value)
        except ValueError:
            config_error("SEED must be a valid integer number.")

    elif key == "PATTERN":
        try:
            number = int(value)
        except ValueError:
            config_error("PATTERN must be either 42 or 1337.")

        config[key] = number


def parse_config(config_path: str = "config.txt") -> Dict[str, Any]:
    """Parse `config_path` and return normalized configuration mapping.

    The returned mapping is also stored in the module-level `config`
    variable.
    """
    raw_config: Dict[str, str] = {}
    try:
        with open(config_path, "r") as config_file:
            for line in config_file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    config_error(
                        "Invalid config line format. Expected: KEY=VALUE"
                    )

                key, value = line.split("=", 1)
                key = key.strip()
                key = key.upper()
                value = value.split("#")[0].strip()

                raw_config[key] = value

        # Check required keys
        for key in config_keys:
            if key not in raw_config:
                config_error(f"Missing required key: {key}")

        # Validate values (writes normalized values into module-level `config`)
        for key in list(raw_config.keys()):
            value_valid(key, raw_config[key])

        check_path()

        config["CONFIG_FILE"] = config_path
        return config

    except FileNotFoundError:
        config_error("Config file not found.")
    except PermissionError:
        config_error("Cannot access config file. Please check permissions.")
    except IsADirectoryError:
        config_error("The config path points to a directory, not a file.")
    except ValueError as e:
        raise ValueError(f"Configuration Error: {e}")
    except Exception as e:
        raise Exception(e)


def parse_maze_output(filename: str) -> Tuple[Matrix, Meta]:
    """Parse a maze output file produced by the generators.

    Returns a tuple `(matrix, meta)` where `matrix` is a 2D list of
    cell bit-lists and `meta` contains optional `entry`, `exit`, and
    `path` information extracted from the file.
    """
    matrix: List[List[List[int]]] = []
    meta: Dict[str, Any] = {}

    try:
        with open(filename, "r") as file:
            lines = [line.strip() for line in file.readlines()]
            i = 0

            # Parse maze grid
            while i < len(lines) and lines[i]:
                row = []
                for c in lines[i]:
                    try:
                        num = int(c, 16)
                    except ValueError:
                        config_error(
                            "Maze file contains invalid hexadecimal"
                            " characters."
                        )

                    bin_str = format(num, "04b")
                    bits = [int(x) for x in bin_str]
                    row.append(bits)

                matrix.append(row)
                i += 1

            # Skip empty lines
            while i < len(lines) and not lines[i]:
                i += 1

            # Parse metadata
            if i + 2 < len(lines):
                try:
                    meta["entry"] = tuple(map(int, lines[i].split(",")))
                    meta["exit"] = tuple(map(int, lines[i + 1].split(",")))
                    meta["path"] = lines[i + 2]
                except ValueError:
                    config_error("Invalid metadata format in maze file.")

    except FileNotFoundError:
        print("Maze output file not found.")
        return [], {}

    return matrix, meta


if __name__ == "__main__":
    parse_config()
