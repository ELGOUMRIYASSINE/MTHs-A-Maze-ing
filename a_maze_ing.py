import parse as parser
from mazegen.kill_hunt_generator import KillHuntGenerator
from mazegen.rec_bt_generator import RecBTGenerator
from Path_finder import maze_solver
from Maze_Display import display
import sys
import os
import pygame

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
    sound = True
    show_path = False
    animate_walk = False
    current_theme_idx = 0
    gen_algo = 1  # 1 for RecBT, 0 for KillHunt

    # Initialize generators once
    maze_rec = RecBTGenerator(parser.config)
    maze_kill = KillHuntGenerator(parser.config)

    # Global state variables
    animation_data = None
    path_coords = None
    path_string = ""

        # 1. Initialize the mixer (you might already have this line!)
    pygame.mixer.init()

    # 2. Load your background music file (can be .mp3 or .wav)
    pygame.mixer.music.load("background_theme.mp3")

    # 3. Set the volume so it doesn't drown out your sound effects!
    # 0.3 means 30% volume. 1.0 is max volume.
    pygame.mixer.music.set_volume(0.15)

    # 4. Play the music!
    # The '-1' tells pygame to loop the music infinitely until the program closes.
    pygame.mixer.music.play(-1)
    def generate_current_maze(reload_state=False):
            global animation_data, path_coords, path_string

            # THE FIX: Create a BRAND NEW instance every time this is called!
            # This guarantees the old history is completely forgotten.
            if gen_algo:
                active_maze = maze_rec
            else:
                active_maze = maze_kill

            # 1. Generate the maze
            if reload_state:
                checker()
                active_maze.reload_config(parser.config)

                # print(parser.config)

            active_maze.generate()

            # 2. Read the true coordinates
            _, meta = display.parse_maze_output(parser.config['OUTPUT_FILE'])

            # 3. Solve using true coordinates
            path_string, path_coords = maze_solver.solve_maze_bfs(
                parser.config['OUTPUT_FILE'],
                meta['entry'],
                meta['exit']
            )

            # 4. Update and get the CLEAN history
            active_maze.update(path_string)
            animation_data = active_maze.get_walk_history()
            with open("history.txt", "a") as file:
                file.write(str(animation_data))
                file.write("\n")

    # Generate the very first maze when the program starts
    generate_current_maze()

    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            # Pass our variables to the display
            display.render_maze(parser.config, show_path, animate_walk, current_theme_idx, path_coords, path_string, animation_data, sound)
            animation_data = None

            C_CYAN = "\033[96m"
            C_GREEN = "\033[92m"
            C_YELLOW = "\033[93m"
            C_MAGENTA = "\033[95m"
            C_RED = "\033[91m"
            C_BOLD = "\033[1m"
            C_RESET = "\033[0m"

            # Dynamically color the ON/OFF status
            anim_status = f"{C_GREEN}ON{C_RESET}" if animate_walk else f"{C_RED}OFF{C_RESET}"
            algo_name = "Recursive Backtracking" if gen_algo else "Kill & Hunt"
            perfect_state = "Perfect" if parser.config['PERFECT'] else "Inperfect"
            sound_status = f"{C_GREEN}ON{C_RESET}" if sound else f"{C_RED}OFF{C_RESET}"
            # The beautifully formatted menu string
            print(f"\n{C_MAGENTA}{C_BOLD}✨ === MTH's A-MAZE-ING === ✨{C_RESET}")
            print(f"{C_CYAN}⚙️  Current Algorithm : {C_YELLOW}{algo_name}{C_RESET}")
            print(f"{C_CYAN}🧩 Maze State        : {C_YELLOW}{perfect_state}{C_RESET}\n") # <--- THE NEW LINE

            print(f"{C_YELLOW}1.{C_RESET} 🎲 Re-generate a new maze")
            print(f"{C_YELLOW}2.{C_RESET} 🗺️  Show/Hide solution path")
            print(f"{C_YELLOW}3.{C_RESET} 🎨 Rotate maze color theme")
            print(f"{C_YELLOW}4.{C_RESET} 🔄 Switch generation algorithm")
            print(f"{C_YELLOW}5.{C_RESET} 🎬 Toggle Path Animation [ {anim_status} ]")
            print(f"{C_YELLOW}6.{C_RESET} 📂 Reload Configuration File")
            print(f"{C_YELLOW}7.{C_RESET} 🔊 Toggle Sound Effects  [ {sound_status} ]")
            print(f"{C_YELLOW}8.{C_RESET} ❌ Quit\n")

            # A sharp, colorful input prompt
            choice = input(f"{C_CYAN}▶ Enter your choice (1-8): {C_RESET}")

            match choice:
                case "1":
                    generate_current_maze()
                case "2":
                    show_path = not show_path
                case "3":
                    current_theme_idx = (current_theme_idx + 1) % len(display.THEMS)
                case "4":
                    gen_algo = not gen_algo
                    generate_current_maze(True)
                case "5":
                    animate_walk = not animate_walk # <--- TOGGLE THE FLAG
                case "6":
                    generate_current_maze(True)
                case "7":
                    if show_path:
                        show_path = not show_path
                    sound = not sound
                    # Instantly pause or unpause the background music!
                    if sound:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                case "8":
                    print("Goodbye!")
                    exit()
                case _:
                    print("Invalid choice")
    except KeyboardInterrupt:
        exit()
