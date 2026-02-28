from collections import deque
import parse as parser

def parse_maze_output(filename):
    matrix = []
    meta = {}
    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
            i = 0

            while i < len(lines) and lines[i]:
                row = []
                for c in lines[i]:
                    value = int(c, 16)
                    value = format(value, "04b")
                    bits = [int(x) for x in value]
                    row.append(bits)
                matrix.append(row)
                i += 1

            while i < len(lines) and not lines[i]:
                i += 1

            if i + 2 < len(lines):
                meta['entry'] = tuple(map(int, lines[i].split(',')))
                meta['exit'] = tuple(map(int, lines[i + 1].split(',')))
                meta['path'] = lines[i + 2]

    except FileNotFoundError:
        print("Error: File not found")
        return [], {}
    return matrix, meta

def create_binary_matrix(output_file):
    hex_matrix, meta = parse_maze_output(output_file)
    if not hex_matrix:
        return

    entry_pos = parser.config['ENTRY']
    exit_pos = parser.config['EXIT']

    height = len(hex_matrix)
    width = len(hex_matrix[0])

    binary_grid = [[1 for _ in range(2 * width + 1)] for _ in range(2 * height + 1)]

    for r in range(height):
        for c in range(width):
            new_r = r * 2 + 1
            new_c = c * 2 + 1

            binary_grid[new_r][new_c] = 0

            west, south, east, north = hex_matrix[r][c]

            if not north:
                binary_grid[new_r - 1][new_c] = 0
            if not south:
                binary_grid[new_r + 1][new_c] = 0
            if not west:
                binary_grid[new_r][new_c - 1] = 0
            if not east:
                binary_grid[new_r][new_c + 1] = 0

    entry_x, entry_y = entry_pos
    exit_x, exit_y = exit_pos

    binary_grid[entry_y * 2 + 1][entry_x * 2 + 1] = 'A'
    binary_grid[exit_y * 2 + 1][exit_x * 2 + 1] = 'B'

    # with open("binary_grid.csv", "w") as f:
    #     for row in binary_grid:
    #         f.write("".join(str(cell) for cell in row) + "\n")
    return binary_grid


def solve_maze_bfs(output_file):
    
    binary_grid = create_binary_matrix(output_file)

    if binary_grid is None:
        print("Stopping: Cannot solve the maze because the matrix is empty (File missing).")
        exit(1)

    raw_start = parser.config['ENTRY']
    raw_exit = parser.config['EXIT']

    # 2. Scale them up to the expanded binary grid!
    # raw[0] is X (column), raw[1] is Y (row)
    # The new coordinate format is (row, col)
    start_pos = (raw_start[1] * 2 + 1, raw_start[0] * 2 + 1)
    exit_pos = (raw_exit[1] * 2 + 1, raw_exit[0] * 2 + 1)

    queue = deque()
    queue.append(start_pos)
    
    visited = set()
    visited.add(start_pos)
    
    parent = {start_pos: None}
    
    while queue:
        current_pos = queue.popleft()

        if current_pos == exit_pos:
            break
            
        r, c = current_pos

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc
        
            if binary_grid[nr][nc] == 0 or binary_grid[nr][nc] == 'B':
                neighbor = (nr, nc)

                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current_pos
                    queue.append(neighbor)
                    
    if exit_pos not in parent:
        return "NO PATH"
    
    path_coords = []
    current = exit_pos

    while current is not None:
        path_coords.append(current)
        current = parent[current]

    path_coords.reverse()
    
    path_string = ""
    for i in range(len(path_coords) - 1):
        r1, c1 = path_coords[i]
        r2, c2 = path_coords[i+1]

        if r2 < r1:
            path_string += "N"
        elif r2 > r1:
            path_string += "S"
        elif c2 > c1:
            path_string += "E"
        elif c2 < c1:
            path_string += "W"
    
    final_path = path_string[::2]
    return final_path, path_coords