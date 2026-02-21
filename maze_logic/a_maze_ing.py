import parse as parser
from kill_hunt_generator import MazeGenerator
from rec_bt_generator import MazeGenerator as RecBTGenerator
import sys

try:
    if len(sys.argv) == 2:
        parser.parse_config(sys.argv[1])
    else:
        parser.parse_config()
except Exception as e:
    print(e)
    exit()
    
if __name__ == "__main__":
    # maze = RecBTGenerator(parser.config)
    maze = MazeGenerator(parser.config)
    maze.generate()

