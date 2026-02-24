import math

config_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
config = {}


def check_path():
    width = config['WIDTH']
    height = config['HEIGHT']
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

    # I'm checking if entry and exit in 42
    pattern = [
        [1, 0, 1, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1]
    ]

    area_h, area_w = 5, 7
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
        if key == 'WIDTH' and (value < 9 or value > 45):
            return ValueError("Invalid value for key:", key)
        if key == 'HEIGHT' and (value < 7 or value > 45):
            raise ValueError("Invalid value for key:", key)
        config[key] = value
    if key in ['ENTRY', 'EXIT']:
        value = value.split(",")
        if len(value) != 2:
            return False
        config[key] = (int(value[0]), int(value[1]))
    if key == 'OUTPUT_FILE':
        try:
            open(value, 'w')
        except Exception:
            raise ValueError("Invalid file for key:", key)
    if key == 'PERFECT':
        if (value == 'True'):
            value = True
        elif (value == 'False'):
            value = False
        else:
            raise ValueError("Invalid value for key:", key)
        config[key] = value


def parse_config(config_path="config.txt"):
    try:
        with open(config_path, 'r') as config_file:
            for line in config_file:
                if (line[0] == '#' or line.strip() == ''):
                    continue
                data = line.split("=")
                if (len(data) != 2 or not data[0] in config_keys):
                    raise ValueError("Invalid config format")
                config[data[0]] = data[1].split("#")[0].rstrip('\n')
            for key in config_keys:
                if key not in config:
                    raise ValueError("Missing key(s) in config")
            for key, value in config.items():
                value_valid(key, value)
            check_path()
    except Exception as e:
        print(e)
        exit()


if __name__ == "__main__":
    parse_config()
