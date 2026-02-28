import math

config_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT', 'SEED']
config = {}


def check_path():
    width = config['WIDTH']
    height = config['HEIGHT']
    if not 'PATTERN' in config:
        config['PATTERN'] = 42
    x, y = config['ENTRY']
    x2, y2 = config['EXIT']

    # here I'm checking if entry and exit in the same point
    if x == x2 and y == y2:
        raise ValueError("Entry or Exit Problem")
    # I'm checking if entry and exit in the grid
    if not (0 <= x <= width - 1 and 0 <= y <= height - 1):
        raise ValueError("ENTRY not on the maze")
    if not (0 <= x2 <= width - 1 and 0 <= y2 <= height - 1):
        raise ValueError("EXIT not on the maze")

    # I'm checking if entry and exit in 42 or 1337
    pattern_42 = [
        [1, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1]
    ]

    pattern_1337 = [
        [0,0,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1],
        [0,1,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1],
        [1,0,1,0,1,1,1,1,0,1,1,1,1,0,0,0,0,0,1],
        [0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1],
        [0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1],
        [0,0,1,0,1,1,1,1,0,1,1,1,1,0,0,0,0,0,1],
    ]
    if config['PATTERN'] == 42:
        pattern = pattern_42
    else:
        pattern = pattern_1337
    area_h, area_w = len(pattern), len(pattern[0])
    start_y = math.floor((config['HEIGHT'] - area_h) / 2)
    start_x = math.floor((config['WIDTH'] - area_w) / 2)

    for p_y in range(area_h):
        for p_x in range(area_w):
            if pattern[p_y][p_x] == 1:
                if start_y + p_y == y and start_x + p_x == x:
                    raise ValueError("ENTRY must be outside 42")
                if start_y + p_y == y2 and start_x + p_x == x2:
                    raise ValueError("ENTRY must be outside 42")


def value_valid(key, value):
    if key in ['WIDTH', 'HEIGHT']:
        value = int(value)
        if key == 'WIDTH' and (value < 9 or value > 100):
            return ValueError("Invalid value for key:", key)
        if key == 'HEIGHT' and (value < 7 or value > 100):
            raise ValueError("Invalid value for key:", key)
        config[key] = value
    if key in ['ENTRY', 'EXIT']:
        value = value.split(",")
        if len(value) != 2:
            return False
        config[key] = (int(value[0]), int(value[1]))
    if key == 'OUTPUT_FILE':
        if not value:
            raise ValueError("No Outputfile Provided")
        try:
            open(value, 'w')
        except PermissionError:
            raise PermissionError("Check Output file permissions ! cant write")
        except ValueError:
            raise ValueError("Invalide Output file Value")
        except IsADirectoryError:
            raise IsADirectoryError("Output file given is a directory")
        except Exception:
            raise Exception("Somthing Went Wrong With Output File Key")
    if key == 'PERFECT':
        if (value == 'True'):
            value = True
        elif (value == 'False'):
            value = False
        else:
            raise ValueError("Invalid value for key:", key)
        config[key] = value
    if key == 'SEED':
        value = int(value)
        if not isinstance(value, int):
            raise ValueError("Invalid value for key:", key)
        config[key] = value
    if key == 'PATTERN':
        number = int(value)
        if number == 42 or number == 1337:
            config[key] = number
        else:
            config[key] = 42


def parse_config(config_path="config.txt"):
    try:
        with open(config_path, 'r') as config_file:
            try:
                for line in config_file:
                    if (line[0] == '#' or line.strip() == ''):
                        continue
                    data = line.split("=")
                    # if (len(data) != 2 or not data[0] in config_keys):
                    if (len(data) != 2):
                        raise ValueError("Invalid config format")
                    config[data[0]] = data[1].split("#")[0].rstrip('\n')
                for key in config_keys:
                    if key not in config:
                        raise ValueError(f"Missing {key} in config file")
                for key, value in config.items():
                    value_valid(key, value)
                check_path()
            except Exception as e:
                print(e)
                exit()
        config['CONFIG_FILE'] = config_path
    except PermissionError:
        raise PermissionError("Check Config File permissions ! Cant Write")
    except ValueError:
        raise ValueError("Invalide Config file Value")
    except IsADirectoryError:
        raise IsADirectoryError("Config file Given Is A Directory")
    except Exception:
        raise Exception("Somthing Went Wrong With Config file Key")

def parse_maze_output(filename):
    matrix = []
    meta = {}
    try:
        with open(filename, 'r') as file:
            lines = [l.strip() for l in file.readlines()]
            i = 0

            # Parse Maze grids
            while i < len(lines) and lines[i]:
                row = []
                for c in lines[i]:
                    value = int(c, 16)
                    value = format(value, "04b")
                    bits = [int(x) for x in value]
                    row.append(bits)
                matrix.append(row)
                i += 1

            # Skip potential empty lines
            while i < len(lines) and not lines[i]:
                i += 1

            # Parse metadata
            if i + 2 < len(lines):
                # Convert coords to integers immediately here for safety
                meta['entry'] = tuple(map(int, lines[i].split(',')))
                meta['exit'] = tuple(map(int, lines[i+1].split(',')))
                meta['path'] = lines[i+2]

    except FileNotFoundError:
        print("Error: File not found")
        return [], {}
    return matrix, meta

if __name__ == "__main__":
    parse_config()
