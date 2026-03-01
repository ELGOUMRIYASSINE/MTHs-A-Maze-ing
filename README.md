# 🧩 Maze Algorithms

A Python package providing multiple maze generation algorithms and a BFS maze solver.

This package allows you to:

- Generate mazes using different algorithms
- Solve mazes using Breadth-First Search (BFS)
- Render mazes in terminal
- Switch between algorithms dynamically
- Visualize walk history
- Toggle path display

---

## 🚀 Installation

If installing locally:

```bash

pip install .

If published on PyPI:

pip install maze-algorithms
📦 Available Algorithms

Currently implemented:

Recursive Backtracking (DFS-based)

Kill & Hunt Algorithm

🧠 How It Works

Each generator:

Takes a configuration dictionary

Generates a maze

Writes output to a file

Can update the maze with a solution path

Stores walk history

⚙️ Configuration

The package expects a configuration dictionary like:

config = {
    "WIDTH": 20,
    "HEIGHT": 20,
    "OUTPUT_FILE": "maze.txt"
}

You can load configuration using your parse_config() function.

🧪 Basic Usage Example
1️⃣ Generate Maze Using Recursive Backtracking
from maze_algorithms.algo_generators.rec_bt_generator import RecBTGenerator

config = {
    "WIDTH": 20,
    "HEIGHT": 20,
    "OUTPUT_FILE": "maze.txt"
}

maze = RecBTGenerator(config)
maze.generate()
2️⃣ Generate Maze Using Kill & Hunt
from maze_algorithms.algo_generators.kill_hunt_generator import KillHuntGenerator

maze = KillHuntGenerator(config)
maze.generate()
3️⃣ Solve Maze Using BFS
from maze_algorithms.algo_generators import maze_solver

path_string, path_coords = maze_solver.solve_maze_bfs("maze.txt")
4️⃣ Update Maze With Solution Path
maze.update(path_string)
5️⃣ Get Walk History
history = maze.get_walk_history()
print(history)
🖥️ Interactive Mode Example

If using your CLI application:

python main.py config.txt

Menu options:

Re-generate maze

Show/Hide solution path

Rotate color theme

Switch generation algorithm

Quit

🧮 Algorithms Explanation
Recursive Backtracking

Depth-First Search based algorithm:

Start from random cell

Mark visited

Randomly visit unvisited neighbors

Backtrack when stuck

Produces perfect mazes (no cycles).

Kill & Hunt

Two-phase algorithm:

Kill phase: Random walk until dead end

Hunt phase: Scan grid to find new unvisited cell

Produces organic-looking mazes.

BFS Solver

Breadth-First Search guarantees shortest path.

Steps:

Start from entry

Explore neighbors level by level

Stop when exit found

Reconstruct path

Time Complexity: O(V + E)

📁 Project Structure
maze_algorithms/
│
├── algo_generators/
│   ├── rec_bt_generator.py
│   ├── kill_hunt_generator.py
│   └── maze_solver.py
│
├── display.py
└── __init__.py
🧑‍💻 Requirements

Python 3.8+

No external dependencies

🔮 Future Improvements

Add Prim's Algorithm

Add Kruskal's Algorithm

Add A* Solver

Add GUI (Pygame or Tkinter)

Publish to PyPI

📜 License

MIT License

👨‍💻 Author

Yassine Elgoumri
Full Stack & Backend Developer


---

# 🧠 Now Let Me Improve You (Professional Level Advice)

To make your package look **serious and publishable**, I recommend:

### ✅ Add:

- Docstrings to every class and method
- Type hints
- `__all__` inside `__init__.py`
- Version number in `__init__.py`
- Proper CLI entry point

Example:

```python
__version__ = "0.1.0"