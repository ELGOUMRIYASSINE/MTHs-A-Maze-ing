import parse as parser
# from maze_logic.algo_generators.kill_hunt_generator import KillHuntGenerator
# from maze_logic.algo_generators.rec_bt_generator import RecBTGenerator
# from maze_logic.algo_generators import maze_solver
from algo_generators.kill_hunt_generator import KillHuntGenerator
from algo_generators.rec_bt_generator import RecBTGenerator
from algo_generators import maze_solver
from Maze_Display import display
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

if __name__ == "__main__":
    # Moved checker inside __main__ so it doesn't run automatically if imported
    checker()

    show_path = False
    current_theme_idx = 0
    gen_algo = 1  # 1 for RecBT, 0 for KillHunt

    # Initialize generators once
    maze_rec = RecBTGenerator(parser.config)
    maze_kill = KillHuntGenerator(parser.config)

    # Global state variables
    animation_data = None
    path_coords = None
    path_string = ""

    def generate_current_maze():
        global animation_data, path_coords, path_string
        active_maze = maze_rec if gen_algo else maze_kill
        
        # 1. Generate the maze
        active_maze.generate()
        
        # 2. Read the file to find where Tom and Jerry actually spawned
        _, meta = display.parse_maze_output(parser.config['OUTPUT_FILE'])
        
        # 3. Pass the true entry/exit to the solver
        path_string, path_coords = maze_solver.solve_maze_bfs(
            parser.config['OUTPUT_FILE'], 
            meta['entry'], 
            meta['exit']
        )
        
        active_maze.update(path_string)
        animation_data = active_maze.get_walk_history()

    # Generate the very first maze when the program starts
    generate_current_maze()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        # Pass our variables to the display
        display.render_maze(parser.config, show_path, current_theme_idx, path_coords, path_string, animation_data)
        
        # THE MAGIC TRICK: Immediately set animation_data to None!
        # This prevents the maze from slowly re-animating when we just change colors or toggle the path.
        animation_data = None

        print("=== A-Maze-ing ===")
        print(f"Algorithm: {'Recursive Backtracking' if gen_algo else 'Kill & Hunt'}")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path")
        print("3. Rotate maze colors")
        print("4. Switch generation algorithm")
        print("5. Quit")

        choice = input("Choice? (1-5): ")

        match choice:
            case "1":
<<<<<<< HEAD
                checker() # Re-parse config if you need fresh width/height
                generate_current_maze()
=======
                # checker()
                if gen_algo:
                    maze.generate()
                    path_string, path_coords = maze_solver.solve_maze_bfs(parser.config['OUTPUT_FILE'])
                    maze.update(path_string)
                else:
                    maze2.generate()
                    path_string, path_coords = maze_solver.solve_maze_bfs(parser.config['OUTPUT_FILE'])
                    maze2.update(path_string)
>>>>>>> 14c7abe8a602cd7dd05d9e56c64ed2e69e9076e6
            case "2":
                show_path = not show_path
            case "3":
                current_theme_idx = (current_theme_idx + 1) % len(display.THEMS)
            case "4":
                gen_algo = not gen_algo
                # Automatically generate a new maze to show off the switched algorithm!
                generate_current_maze() 
            case "5":
                print("Goodbye!")
                exit()
            case _:
                print("Invalid choice")