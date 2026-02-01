config_path = "./config.txt"
config = {}


keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
def read_config():
    try:
        with open(config_path, 'r') as config_file:
            for line in config_file:
                data = line.split("=")
                if (len(data) != 2 or not data[0] in keys):
                        raise ValueError
                config[data[0]] = data[1].rstrip('\n')
    except (FileNotFoundError, ValueError):
        print("Error Found Parsing!")
        exit()

read_config()
# print(config['ENTRY'])
