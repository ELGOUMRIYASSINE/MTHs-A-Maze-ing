import time

def parse_to_matrix(filename):
    matrix = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                clean_line = line.strip()
                if not clean_line: continue

                row = []
                for c in clean_line:
                    value = int(c, 16)
                    value = format(value, "04b")
                    bits = [int(x) for x in value]
                    row.append(bits)
                matrix.append(row)

    except FileNotFoundError:
        print("Error: File not found")
        return []

    return matrix

CHAR = "█"
SPACE = " "

def render_maze():
    matrix = parse_to_matrix("../maze_output.txt")
    for row in matrix:
        line_top = ""
        line_mid = ""
        for cell in row:
            west, south, east, north = cell
            line_top += CHAR
            line_top += CHAR * 3 if north else SPACE * 3

            line_mid += CHAR if west else SPACE
            line_mid += SPACE * 3

        line_top += CHAR
        line_mid += CHAR

        print(line_top)
        print(line_mid)

    line_bot = ""
    last_row = matrix[-1]

    for cell in last_row:
        west, south, east, north = cell
        line_bot += CHAR
        line_bot += CHAR * 3 if south else SPACE * 3

    line_bot += CHAR
    print(line_bot)

if __name__ == "__main__":
    render_maze()
