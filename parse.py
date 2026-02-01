config_path = "./config.txt"
config = {}
config_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']


def value_valid(key, value):
    if key in ['WIDTH', 'HEIGHT']:
        value = int(value)
        if not (value <= 100 and value >= 5):
            raise ValueError("Invalid value for key:", key)
        config[key] = value
    if key in ['ENTRY', 'EXIT']:
        value = value.split(",")
        if len(value) != 2:
            return False
        x, y = int(value[0]), int(value[1])
        if (not (((x == int(config.get('WIDTH', 0)) -1  or x == 0)) and ((y == int(config.get('HEIGHT', 0)) -1  or y == 0)))):
            raise ValueError("Invalid value for key:", key)
        config[key] = (x, y)
    if key == 'OUTPUT_FILE':
        try:
            open(value, 'r')
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


def parse_config():
    try:
        with open(config_path, 'r') as config_file:
            for line in config_file:
                data = line.split("=")
                if (len(data) != 2 or not data[0] in config_keys):
                        raise ValueError("Invalid config format")
                config[data[0]] = data[1].rstrip('\n')
            for key in config_keys:
                if key not in config:
                    raise ValueError("Missing key(s) in config")
            for key, value in config.items():
                value_valid(key, value)
                if config['ENTRY'] == config['EXIT']:
                    raise ValueError("The Entry The Same As The Exit!!!")
    except Exception as e:
        print(e)
        exit()

parse_config()
print(config)