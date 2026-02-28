import parse as parser
from maze_logic.kill_hunt_generator import KillHuntGenerator
from maze_logic.rec_bt_generator import RecBTGenerator
from maze_logic import maze_solver
from Maze_Display import display
# from maze_logic.Cell import Cell
import sys
import os


def checker():
    try:
        if len(sys.argv) == 2:
            parser.parse_config(sys.argv[1])
        else:
            parser.parse_config()
    except Exception as e:
        print(e)
        exit()


checker()

if __name__ == "__main__":
    show_path = False
    current_theme_idx = 0
    gen_algo = 1

    maze = RecBTGenerator(parser.config)
    maze.generate()
    path_string, path_coords = maze_solver.solve_maze_bfs(parser.config['OUTPUT_FILE'])
    maze.update(path_string)

    maze2 = KillHuntGenerator(parser.config)
    maze2.generate()
    path_string, path_coords = maze_solver.solve_maze_bfs(parser.config['OUTPUT_FILE'])
    maze2.update(path_string)

    print(maze2.get_walk_history())

    while True:
        # Clear screen (Optional, makes it look like a game)
        os.system('cls' if os.name == 'nt' else 'clear')

        display.render_maze(parser.config, show_path, current_theme_idx, path_coords, path_string)
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path")
        print("3. Rotate maze colors")
        print("4. Switch generation algorithm")
        print("5. Quit")

        choice = input("Choice? (1-5): ")

        match choice:
            case "1":
                checker()
                if gen_algo:
                    maze.generate()
                    path_string, path_coords = maze_solver.solve_maze_bfs(parser.config['OUTPUT_FILE'])
                    maze.update(path_string)
                else:
                    maze2.generate()
                    path_string, path_coords = maze_solver.solve_maze_bfs(parser.config['OUTPUT_FILE'])
                    maze2.update(path_string)
            case "2":
                show_path = not show_path  # Toggle flag
            case "3":
                current_theme_idx = (current_theme_idx + 1) % len(display.THEMS)
            case "4":
                gen_algo = not gen_algo
            case "5":
                exit()
            case _:
                print("Invalid choice")

