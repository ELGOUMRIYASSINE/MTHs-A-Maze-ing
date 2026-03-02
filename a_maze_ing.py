import os
import sys
from typing import Any

import parse as parser
from Maze_Display import display
from Path_finder import maze_solver
from mazegen.MazeGenerator import MazeGenerator
from mazegen.kill_hunt_generator import KillHuntGenerator
from mazegen.rec_bt_generator import RecBTGenerator

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame  # noqa: E402

AnimationStep = tuple[int, int, str]
PathCoord = tuple[int, int]


def _normalize_animation_data(raw_history: Any) -> list[AnimationStep] | None:
    if not isinstance(raw_history, list):
        return None

    normalized: list[AnimationStep] = []
    for step in raw_history:
        if not isinstance(step, (list, tuple)) or len(step) != 3:
            continue
        row, col, direction = step
        if isinstance(row, int) and isinstance(col, int) and isinstance(
            direction,
            str,
        ):
            normalized.append((row, col, direction))

    return normalized


def checker(reloading: bool = False) -> None:

    try:
        if len(sys.argv) == 2:
            parser.parse_config(sys.argv[1])
        else:
            parser.parse_config()
    except Exception as e:
        print(e)
        if not reloading:
            exit()
        raise Exception(e)


if __name__ == "__main__":
    # Moved checker inside __main__ so it doesn't run automatically if imported
    checker()
    Warning_stat = None
    sound = True
    show_path = False
    animate_walk = False
    current_theme_idx = 0
    gen_algo = 1  # 1 for RecBT, 0 for KillHunt

    # Initialize generators once
    maze_rec = RecBTGenerator(parser.config)
    maze_kill = KillHuntGenerator(parser.config)

    # Global state variables
    animation_data: list[AnimationStep] | None = None
    path_coords: list[PathCoord] | None = None
    path_string = ""

    # 1. Initialize the mixer (you might already have this line!)
    pygame.mixer.init()

    # 2. Load your background music file (can be .mp3 or .wav)
    pygame.mixer.music.load("sounds/background_theme.mp3")

    # 3. Set the volume so it doesn't drown out your sound effects!
    # 0.3 means 30% volume. 1.0 is max volume.
    pygame.mixer.music.set_volume(0.15)

    # 4. Play the music!
    # The '-1' tells pygame to loop the music infinitely.
    pygame.mixer.music.play(-1)

    def generate_current_maze(reload_state: bool = False) -> None:
        global animation_data, path_coords, path_string, Warning_stat
        Warning_stat = None  # Reset at start

        if gen_algo:
            active_maze: MazeGenerator = maze_rec
        else:
            active_maze = maze_kill

        # 1. Handle config reload
        if reload_state:
            try:
                old_config = parser.config.copy()
                checker(True)
                active_maze.reload_config(parser.config)
            except Exception as e:
                Warning_stat = str(e)  # Save reload error
                parser.config = old_config
                active_maze.reload_config(parser.config)

        # 2. Generate the maze
        active_maze.generate()

        # 3. Check will_draw (keep existing warning if reload already failed).
        if not active_maze.will_draw:
            if Warning_stat:
                Warning_stat = (
                    f"{Warning_stat} | {active_maze.pattern} "
                    "can't be drawn on small grid"
                )
            else:
                Warning_stat = (
                    f"{active_maze.pattern} can't be drawn on small grid"
                )

        # 4. Read the true coordinates
        _, meta = display.parse_maze_output(parser.config['OUTPUT_FILE'])

        # 5. Solve using true coordinates
        solve_result = maze_solver.solve_maze_bfs(
            parser.config['OUTPUT_FILE'],
            meta['entry'],
            meta['exit'],
        )
        if isinstance(solve_result, str):
            path_string = ""
            path_coords = None
        else:
            path_string, path_coords = solve_result

        # 6. Update and get the CLEAN history
        active_maze.update(path_string)
        animation_data = _normalize_animation_data(
            active_maze.get_walk_history()
        )

    generate_current_maze()

    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            # Pass our variables to the display
            display.render_maze(
                parser.config,
                show_path,
                animate_walk,
                current_theme_idx,
                path_coords,
                path_string,
                animation_data,
                sound,
            )
            animation_data = None

            C_CYAN = "\033[96m"
            C_GREEN = "\033[92m"
            C_YELLOW = "\033[93m"
            C_MAGENTA = "\033[95m"
            C_RED = "\033[91m"
            C_BOLD = "\033[1m"
            C_RESET = "\033[0m"

            # Dynamically color the ON/OFF status
            anim_status = (
                f"{C_GREEN}ON{C_RESET}"
                if animate_walk
                else f"{C_RED}OFF{C_RESET}"
            )
            algo_name = "Recursive Backtracking" if gen_algo else "Kill & Hunt"
            perfect_state = (
                "Perfect" if parser.config['PERFECT'] else "Inperfect"
            )
            sound_status = (
                f"{C_GREEN}ON{C_RESET}" if sound else f"{C_RED}OFF{C_RESET}"
            )
            # The beautifully formatted menu string
            print(
                f"\n{C_MAGENTA}{C_BOLD}✨ === MTH's A-MAZE-ING === ✨"
                f"{C_RESET}"
            )
            print(
                f"{C_CYAN}⚙️  Current Algorithm : {C_YELLOW}"
                f"{algo_name}{C_RESET}"
            )
            print(
                f"{C_CYAN}🧩 Maze State        : {C_YELLOW}"
                f"{perfect_state}{C_RESET}\n"
            )

            print(f"{C_YELLOW}1.{C_RESET} 🎲 Re-generate a new maze")
            print(f"{C_YELLOW}2.{C_RESET} 🗺️  Show/Hide solution path")
            print(f"{C_YELLOW}3.{C_RESET} 🎨 Rotate maze color theme")
            print(f"{C_YELLOW}4.{C_RESET} 🔄 Switch generation algorithm")
            print(
                f"{C_YELLOW}5.{C_RESET} 🎬 Toggle Path Animation "
                f"[ {anim_status} ]"
            )
            print(f"{C_YELLOW}6.{C_RESET} 📂 Reload Configuration File")
            print(
                f"{C_YELLOW}7.{C_RESET} 🔊 Toggle Sound Effects  "
                f"[ {sound_status} ]"
            )
            print(f"{C_YELLOW}8.{C_RESET} ❌ Quit\n")
            if Warning_stat:
                print(f"{C_YELLOW}error:{C_RESET} {Warning_stat}\n")
            # A sharp, colorful input prompt
            choice = input(f"{C_CYAN}▶ Enter your choice (1-8): {C_RESET}")

            match choice:
                case "1":
                    generate_current_maze()
                case "2":
                    show_path = not show_path
                case "3":
                    current_theme_idx = (
                        (current_theme_idx + 1) % len(display.THEMS)
                    )
                case "4":
                    gen_algo = not gen_algo
                    generate_current_maze(True)
                case "5":
                    animate_walk = not animate_walk
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
