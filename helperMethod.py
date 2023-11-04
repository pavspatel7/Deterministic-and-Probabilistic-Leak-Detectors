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
    # index = 0 : for finding the neighbors of ' ❌ '  
    if index == 0:
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and grid[nx][ny] != "⬛️" and grid[nx][ny] != "⬜️" and (grid[nx][ny] == "❌" or grid[nx][ny] == "😀" or grid[nx][ny] == "🟥")]
    
    # index = 1 : for finding the neighbors of ' ✅ '
        # Used in Bot - 1 :- At..   
    if index == 1:
        return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and grid[nx][ny] != "⬛️" and (grid[nx][ny] == "✅" or grid[nx][ny] == "😀")]
    
    # index = 1 : for finding the neighbors not including the Block cells
        # Used in Bot - 2 :- At..
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
        if 0 <= nx < len(grid) and 0 <= ny < len(grid) and (grid[nx][ny] == "⬜️" or grid[nx][ny] == "🟥" or grid[nx][ny] == "❌"):
            return True
    return False


def out_cells_bot_2(k, grid, botpos):

    tempGrid = [row.copy() for row in grid]
    # Calculate Outer distance
    outercell_distance =  k + 1  # Twice the first detection grid
    temp = outer_detection_cells(tempGrid)
    outermost_green_cell = []
    for (x,y) in temp:
        if  0 <= x < len(tempGrid) and 0 <= y+outercell_distance < len(tempGrid) and tempGrid[x][y] == "✅" and tempGrid[x][y+outercell_distance] == "⬜️":
            tempGrid[x][y+outercell_distance] = "🔵"
            outermost_green_cell.append((x,y+outercell_distance))
        if  0 <= x-outercell_distance < len(tempGrid) and 0 <= y < len(tempGrid) and tempGrid[x][y] == "✅" and tempGrid[x-outercell_distance][y] == "⬜️":
            tempGrid[x-outercell_distance][y] = "🔵"
            outermost_green_cell.append((x-outercell_distance,y))
        if  0 <= x+outercell_distance < len(tempGrid) and 0 <= y < len(tempGrid) and tempGrid[x][y] == "✅" and tempGrid[x+outercell_distance][y] == "⬜️":
            tempGrid[x+outercell_distance][y] = "🔵"
            outermost_green_cell.append((x+outercell_distance,y))
        if  0 <= x < len(tempGrid) and 0 <= y-outercell_distance < len(tempGrid) and tempGrid[x][y] == "✅" and tempGrid[x][y-outercell_distance] == "⬜️":
            tempGrid[x][y-outercell_distance] = "🔵"
            outermost_green_cell.append((x,y-outercell_distance))

    print("**********************")
    for x in tempGrid:
        print(''.join(x))
    print("**********************")
    print()



    #outermost_green_cell = outer_detection_cells_1(tempGrid)
    print("outer",outermost_green_cell)
    return outermost_green_cell


def find_min_distance_and_path(your_dict):
    min_distance = 0 # float('inf')  # Initialize with positive infinity to find the minimum
    min_distance_path = []

    for key, value in your_dict.items():
        distance, path = value
        if distance > 0 and distance > min_distance:
            min_distance = distance
            min_distance_path = path
            #min_distance_key = key

    return min_distance, min_distance_path


