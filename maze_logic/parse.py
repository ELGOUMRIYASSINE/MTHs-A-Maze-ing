config_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
config = {}


def check_path():
    width = config['WIDTH']
    height = config['HEIGHT']
    x, y = config['ENTRY']
    x2, y2 = config['EXIT']
    if not (x == 0 or x == width - 1 or y == 0 or y == height - 1):
        raise ValueError("ENTRY must be on the maze border")
    if not (x2 == 0 or x2 == width - 1 or y2 == 0 or y2 == height - 1):
        raise ValueError("EXIT must be on the maze border")
    if x == x2 and y == y2:
        raise ValueError("Entry or Exist Probleme")


def value_valid(key, value):
    if key in ['WIDTH', 'HEIGHT']:
        value = int(value)
        if not (value <= 45 and value >= 8):
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
                config[data[0]] = data[1].rstrip('\n')
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
