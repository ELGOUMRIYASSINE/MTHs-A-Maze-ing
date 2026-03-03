# mazegen

`mazegen` is the maze-generation package used by this project.
It provides a common base class plus two generation algorithms:

- `RecBTGenerator` (recursive backtracking)
- `KillHuntGenerator` (hunt-and-kill)

The package generates a maze grid, writes it to an output file, and keeps
walk history that can be used by your display/animation layer.

## Requirements

- Python `>= 3.9`
- Standard library only for generation (`random`, `math`, etc.)

## Install / Import

From the repository root:

```bash
pip install -e .
```

You can either work with the concrete generators directly, or use the
high-level `MazeGenerator` facade:

```python
# Recommended: go through the factory facade
from mazegen.MazeGenerator import MazeGenerator

# Or direct imports of concrete generators if needed
from mazegen.rec_bt_generator import RecBTGenerator
from mazegen.kill_hunt_generator import KillHuntGenerator
```

## `BaseGenerator` abstract class

`BaseGenerator` is the abstract base class used by all algorithms in this
package.

- It defines the shared configuration parsing (`HEIGHT`, `WIDTH`, other
  fields).
- It owns the maze grid (`self.grid`) and walk history (`self.walk_history`).
- It handles file output through `update()`.

Abstract methods (must be implemented by subclasses):

- `generate()`: run the full generation process.
- `kill(pos)`: algorithm-specific carving/walk behavior (for algorithms
  that use a kill phase).

Common inherited methods:

- `get_grid()`
- `get_walk_history()`
- `reload_config(config)`
- `update(path_string=None)`

## `MazeGenerator` facade

The `mazegen/MazeGenerator.py` module exposes a small factory class that
creates properly configured generator instances for the supported
algorithms:

- `MazeGenerator.rec_bt_generator(config)` → `RecBTGenerator`
- `MazeGenerator.kill_hunt_gen(config)` → `KillHuntGenerator`

This is what the main CLI entrypoint (`a_maze_ing.py`) uses.

Example:

```python
from mazegen.MazeGenerator import MazeGenerator

factory = MazeGenerator()

rec_bt_gen = factory.rec_bt_generator(config)
kill_hunt_gen = factory.kill_hunt_gen(config)

rec_bt_gen.generate()
kill_hunt_gen.generate()
```

Both returned objects are concrete subclasses of `BaseGenerator`.

## Required configuration

Each generator expects a `config` dictionary.

Strict minimum keys (required by `BaseGenerator.__init__`):

- `HEIGHT` (int)
- `WIDTH` (int)
- `ENTRY` (list[int])
- `EXIT` (list[int])
- `PERFECT` (bool)
- `OUTPUT_FILE` (str)

Common optional keys:

- `SEED` (int): deterministic generation seed, default `0`
- `PATTERN` (int): decorative blocked pattern mode (`42` or `1337`)

Example config:

```python
config = {
  "WIDTH": 30,
  "HEIGHT": 20,
  "ENTRY": [0, 0],
  "EXIT": [29, 19],
  "SEED": 12345,
  "PERFECT": True,
  "OUTPUT_FILE": "maze_output",
  "PATTERN": 42,
}
```

## How the package works

1. Create a generator instance (either via `MazeGenerator` or directly).
2. Call `generate()`.
3. The internal grid is built and carved.
4. Maze data is written to `OUTPUT_FILE`.
5. You can read `walk_history` for animation.

The output file includes:

- maze rows in hexadecimal-cell format,
- then `entry` and `exit` coordinates,
- and optionally a solution path string when `update(path_string=...)` is used.

## Usage examples

### 1) Generate with Recursive Backtracking (via factory)

```python
from mazegen.MazeGenerator import MazeGenerator

factory = MazeGenerator()
generator = factory.rec_bt_generator(config)
generator.generate()

grid = generator.get_grid()
history = generator.get_walk_history()
print(f"Generated {len(grid)}x{len(grid[0])} maze")
print(f"History steps: {0 if history is None else len(history)}")
```

### 2) Generate with Hunt-and-Kill (via factory)

```python
from mazegen.MazeGenerator import MazeGenerator

factory = MazeGenerator()
generator = factory.kill_hunt_gen(config)
generator.generate()
```

### 3) Regenerate with a new config

```python
from mazegen.MazeGenerator import MazeGenerator

factory = MazeGenerator()
generator = factory.rec_bt_generator(config)

generator.generate()

new_config = {**config}
generator.reload_config(new_config)
generator.generate()
```

### 4) Write a solution path into the output file

```python
# Example path from your solver layer
path_string = "NNEESSWW"
generator.update(path_string=path_string)
```

## Choosing an algorithm

- `RecBTGenerator`: fast, classic depth-first style carving.
- `KillHuntGenerator`: different corridor distribution and maze texture.

Both share the same config shape and public interface (`generate`, `update`,
`get_grid`, `get_walk_history`, `reload_config`) via the `BaseGenerator`
base class and can be obtained conveniently through the `MazeGenerator`
factory.