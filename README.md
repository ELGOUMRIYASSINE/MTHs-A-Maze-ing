*This project has been created as part of the 42 curriculum by yelgoumr, ayfadli*
# MTH's A-MAZE-ING

Terminal maze generator and solver project with interactive visualization.

#  Description

## What this project does

- Generates mazes with two algorithms:
    - Recursive Backtracking
    - Hunt-and-Kill
- Solves the generated maze with BFS (shortest path).
- Renders the maze in terminal with theme switching and optional animation.
- Plays background music/effects through `pygame`.

### Why these algorithms?

- **Recursive Backtracking**: simple to implement, guarantees perfect mazes (one unique path between any two cells), and is well suited for step‑by‑step visualization.
- **Hunt-and-Kill**: offers a different maze style and randomness pattern while still producing perfect mazes, which makes side‑by‑side comparison interesting.
- **BFS solver**: breadth‑first search naturally finds the shortest path in an unweighted grid and is easy to reason about and animate level by level.

## Project layout

- `a_maze_ing.py`: main interactive CLI application.
- `parse.py`: config parsing and validation.
- `mazegen/`: reusable generation package.
- `Path_finder/maze_solver.py`: BFS solver.
- `Maze_Display/display.py`: terminal rendering and animation.
- `config.txt`: default runtime config.
- `requirements.txt`: runtime dependencies.

Detailed package docs are in `mazegen/README.md`.

## Reusable components

The maze generation engine is packaged in `mazegen/` so it can be reused in other projects:

- Import the generator class and call it with your own dimensions and configuration.
- Use the returned grid/graph structure as input for different solvers or visualizations.

Example usage from another Python script:

```python
from mazegen.RecBTGenerator import RecBTGenerator

generator = RecBTGenerator(config={
    'WIDTH': 20,
    'HEIGHT': 20,
    'ENTRY': (0, 0),
    'EXIT': (19, 19),
    'PERFECT': True,
    'SEED': 1,
})

maze = generator.generate()
```

This separation allows you to plug the same generation logic into GUIs, web apps, or additional analysis tools without relying on the CLI.

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

## Run the project (Instructions)

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

## Team & project management

### Team members

- **yelgoumr**
    - Implemented recursive backtracking generator
    - Implemented Hunt-and-Kill generator
    - Implemented configuration parser
    - Implemented runtime config reload
    - Built reusable `mazegen` package
    - Handled packaging structure
    - Ensured algorithm abstraction

- **ayfadli**
    - Implemented BFS pathfinder
    - Implemented shortest path visualization
    - Implemented terminal display system
    - Implemented animation system
    - Integrated solver with generator history

### Planning

**Initial plan**

1. Build generator
2. Add solver
3. Add display
4. Add animation
5. Add sound
6. Refactor into reusable modules

**Evolution**

- Started as a single-file design
- Refactored into a modular architecture
- Extracted generation logic into a dedicated package
- Added configuration hot-reload feature
- Improved separation of concerns between generation, solving, display, and config

### What worked well

- Modular architecture
- Clear responsibility separation
- Reusable generation engine
- Animation history tracking

### What could be improved

- Add unit tests
- Add benchmarking
- Improve CLI UX
- Add more algorithms (Prim, Kruskal)

### Tools used

- Python 3
- `flake8`
- `mypy`
- `make`
- `pygame`
- Git
- Terminal ANSI rendering

## Advanced features

- Multiple generation algorithms
- Shortest path solving (BFS)
- Interactive CLI menu
- Theme switching
- Animated solving
- Sound toggle
- Runtime config reload
- Perfect maze option
- Seed control for reproducibility

## Resources

**Maze generation**

- Recursive Backtracking: https://en.wikipedia.org/wiki/Maze_generation_algorithm
- Hunt-and-Kill: https://weblog.jamisbuck.org/2011/1/24/

**BFS**

- Documentation: https://en.wikipedia.org/wiki/Breadth-first_search
- Video: https://www.youtube.com/watch?v=KiCBXu4P-2Y

**Python packaging**

- Guide: https://packaging.python.org/en/latest/tutorials/packaging-projects/

## AI usage

AI tools were used for:

- Algorithm comparison research
- Documentation structure improvement
- Code review suggestions
- Refactoring recommendations
- Error explanation assistance

AI was not used to directly generate full project logic without understanding. All algorithms were implemented manually and validated by testing.

## Conclusion

This project demonstrates:

- Strong algorithmic implementation
- Clean architecture principles
- Runtime safety validation
- Modular design
- Real-world packaging practice

It reflects collaborative teamwork and a structured engineering approach aligned with the 42 curriculum philosophy.

## Troubleshooting

- `Config file not found`: run from repository root or pass config path explicitly.
- `Configuration Error`: verify required keys and value formats in config file.
- No sound / mixer errors: ensure system audio backend is available, or turn sound off.
- Display glitches: use a terminal with ANSI + Unicode support.

## Maze generation architecture

Maze generation is built around three core concepts:

- **`BaseGenerator`**  
  An abstract base class (in `mazegen/BaseGenerator.py`) that defines
  common behaviour for all maze-generation algorithms (grid handling,
  seeding, walk history, imperfect maze post-processing, etc.).

- **Concrete generators**  
  - `KillHuntGenerator` (`mazegen/kill_hunt_generator.py`): implements
    the hunt-and-kill algorithm.
  - The recursive-backtracking generator (`mazegen/rec_bt_generator.py`):
    implements the recursive backtracking algorithm.

  Both classes inherit from `BaseGenerator`.

- **`MazeGenerator` facade**  
  The `mazegen/MazeGenerator.py` module exposes a `MazeGenerator` class
  that acts as a small factory for algorithm-specific generators:

  ```python
  from mazegen.MazeGenerator import MazeGenerator
  import parse as parser

  # parse_config() populates parser.config
  parser.parse_config()

  factory = MazeGenerator()
  rec_bt_gen = factory.rec_bt_generator(parser.config)
  kill_hunt_gen = factory.kill_hunt_gen(parser.config)

  # Each returned object is a BaseGenerator subclass:
  rec_bt_gen.generate()
  kill_hunt_gen.generate()
  ```

  The CLI entrypoint (`a_maze_ing.py`) uses this facade to construct
  generators instead of instantiating algorithm classes directly.

## Extending with new algorithms

To add a new maze-generation algorithm:

1. Implement a new class that inherits from `BaseGenerator`.
2. Implement the required abstract methods (e.g. `generate()`).
3. Optionally expose a convenience constructor in
   `mazegen/MazeGenerator.MazeGenerator` (similar to
   `rec_bt_generator()` and `kill_hunt_gen()`).
