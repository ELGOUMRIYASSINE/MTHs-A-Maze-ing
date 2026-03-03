*This project has been created as part of the 42 curriculum by yelgoumr, ayfadli*
# MTH's A-MAZE-ING

Terminal maze generator and solver project with interactive visualization.

## What this project does

- Generates mazes with two algorithms:
    - Recursive Backtracking
    - Hunt-and-Kill
- Solves the generated maze with BFS (shortest path).
- Renders the maze in terminal with theme switching and optional animation.
- Plays background music/effects through `pygame`.

## Project layout

- `a_maze_ing.py`: main interactive CLI application.
- `parse.py`: config parsing and validation.
- `mazegen/`: reusable generation package.
- `Path_finder/maze_solver.py`: BFS solver.
- `Maze_Display/display.py`: terminal rendering and animation.
- `config.txt`: default runtime config.
- `requirements.txt`: runtime dependencies.

Detailed package docs are in `mazegen/README.md`.

## Requirements

- Python 3.9+
- `pip`
- Terminal that supports ANSI colors and Unicode
- Audio support for `pygame.mixer` (optional, can be toggled in app)

## Dependencies

Runtime:

- `pygame` (listed in `requirements.txt`)

Install dependencies from repository root:

```bash
python3 -m pip install -r requirements.txt
```

Optional (for lint/type checks used in this repo):

```bash
python3 -m pip install mypy flake8
```

Optional editable install of local package:

```bash
python3 -m pip install -e .
```

## Configuration

By default the app reads `config.txt`. You can also pass a custom file path.

Required keys in config file:

- `WIDTH`
- `HEIGHT`
- `ENTRY`
- `EXIT`
- `OUTPUT_FILE`
- `PERFECT`

Optional key:

- `PATTERN` (recommended values: `42` or `1337`)
- `SEED`

Example:

```ini
WIDTH=20
HEIGHT=20
ENTRY=0,0
EXIT=19,19
OUTPUT_FILE=maze_output
PERFECT=True
SEED=1
PATTERN=42
```

## Run the project

From repository root:

```bash
python3 a_maze_ing.py
```

Use a custom config file:

```bash
python3 a_maze_ing.py path/to/config.txt
```

The app opens an interactive menu where you can:

- regenerate a maze,
- show/hide solution path,
- rotate themes,
- switch generation algorithm,
- toggle path animation,
- reload config,
- toggle sound.

## Notes about audio files

The CLI expects these assets to exist:

- `sounds/background_theme.mp3`
- `sounds/meow.mp3`

If audio causes issues in your environment, disable sound from the in-app menu.

## Development commands

Using `makefile` targets:

```bash
make run
make lint
make clean
```

Equivalent direct commands:

```bash
python3 -m flake8 .
python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

## Troubleshooting

- `Config file not found`: run from repository root or pass config path explicitly.
- `Configuration Error`: verify required keys and value formats in config file.
- No sound / mixer errors: ensure system audio backend is available, or turn sound off.
- Display glitches: use a terminal with ANSI + Unicode support.
