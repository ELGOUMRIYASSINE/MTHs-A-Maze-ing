def create_binary_matrix(hex_matrix, entry_pos, exit_pos):

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

    return binary_grid
