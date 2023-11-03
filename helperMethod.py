from collections import deque


# Creating an dection layout based on the current position of the Grid by co-ordinates..
def CreateDetector(k, grid, botpos):
    innerGridCells = []
    x_bot, y_bot = botpos
    detectorGridSize = (2*k + 1)
    halfSize = (detectorGridSize - 1) // 2
    x1 = x_bot - halfSize
    y1 = y_bot - halfSize
    for i in range(detectorGridSize):
        for j in range(detectorGridSize):
            # Calculate the coordinates of each cell in the inner grid
            inner_x = x1 + i
            inner_y = y1 + j
            # Check if the inner_x and inner_y are within the bounds of the size of the grid and not block cells
            if 0 <= inner_x < len(grid) and 0 <= inner_y < len(grid) and grid[inner_x][inner_y] != "⬛️":
                innerGridCells.append((inner_x, inner_y))
    return innerGridCells

# Returns the grid in 2D form used inside the 
def create_mini_grid(k, grid, botpos):
    x, y = botpos
    mini_grid_size = (2*k + 1)
    half_size = (mini_grid_size )// 2

    min_x = max(0, x - half_size)
    max_x = min(len(grid[0]) - 1, x + half_size)
    min_y = max(0, y - half_size)
    max_y = min(len(grid)-1, y + half_size)

    mini_grid = []
    for i in range(min_x, max_x + 1):
        row = []
        for j in range(min_y, max_y + 1):
            row.append(grid[i][j])
        mini_grid.append(row)
    return mini_grid

def find_shortest_path(index, original_grid, bot_no, start, end):
    queue = deque([(start, [])])
    visited = set()
    visited_dfs = set()
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path
        if (x, y) not in visited:
            visited.add((x, y))
            visited_dfs.add((x, y))
            for nx, ny in get_neighbors(index,original_grid, x, y):
                if is_valid_move_bot(original_grid, bot_no, nx, ny):
                    queue.append(((nx, ny), path + [(nx, ny)]))
            visited_dfs.remove((x, y))
    return -1

# Method for Outer safe cell
def outer_detection_cells(grid):
    outer_cells_list = []
    # 1) Get all the safe cells of the originalGrid
    outer_cells = [(i, j) for i in range(len(grid)) for j in range(len(grid)) if grid[i][j] == "✅"]
    for x, y in outer_cells:
        if is_outer_detection(grid, x, y):
            outer_cells_list.append((x, y))
    
    return outer_cells_list

# Helpers of Methods
def get_neighbors(index, grid, x, y):
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    # index = 0 : for finding the neighbors of ' ❎ '  
    if index == 0:
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and grid[nx][ny] != "⬛️" and (grid[nx][ny] == "❎" or grid[nx][ny] == "😀" or grid[nx][ny] == "🟥")]
    # index = 1 : for finding the neighbors of ' ✅ ' 
    if index == 1:
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and grid[nx][ny] != "⬛️" and (grid[nx][ny] == "✅" or grid[nx][ny] == "😀")]
    # index = 1 : for finding the neighbors of ' ✅ ' 
    if index == 2:
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and grid[nx][ny] != "⬛️"]


# Give the validity of the move for the BFS
def is_valid_move_bot(grid,bot_no, x, y):
    if bot_no == 1:
        return 0 <= x < len(grid) and 0 <= y < len(grid) and grid[x][y] != "⬛️"

# This Out detection checks for the out cells of the detection Grid
def is_outer_detection(grid, x, y):
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for nx, ny in neighbors:
        if 0 <= nx < len(grid) and 0 <= ny < len(grid) and (grid[nx][ny] == "⬜️" or grid[nx][ny] == "🟥"):
            return True
    return False