from collections import deque
innerGridCells = []

class help():
    # Creating an dection layout based on the current position of the Grid..
    def CreateDetector(k,sizeOfGrid, grid, x_bot, y_bot):
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
                if 0 <= inner_x < sizeOfGrid and 0 <= inner_y < sizeOfGrid and grid[inner_x][inner_y] != "⬛️":
                    innerGridCells.append((inner_x, inner_y))
        return innerGridCells

    def find_shortest_path(original_grid, start, end):
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
                for nx, ny in get_neighbors(original_grid, x, y):
                    if is_valid_move_bot(original_grid, nx, ny):
                        queue.append(((nx, ny), path + [(nx, ny)]))
                visited_dfs.remove((x, y))
        return None

    # Method for Outer Fire
    def outer_fire_cells(originalGrid):
        outer_fire_cells = []
        # 1) Get all the fire cells of the originalGrid
        fire_cells = [(i, j) for i in range(len(originalGrid)) for j in range(len(originalGrid)) if originalGrid[i][j] == "🔥"]
        for x, y in fire_cells:
            if is_outer_fire(originalGrid, x, y):
                outer_fire_cells.append((x, y))
        return outer_fire_cells


# Helpers of Methods
def get_neighbors(grid, x, y):
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(grid) and 0 <= ny < len(grid) and grid[nx][ny] != "⬛️"]

def is_valid_move_bot(grid, x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid) and grid[x][y] != "⬛️"

def is_outer_fire(grid, x, y):
    neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for nx, ny in neighbors:
        if 0 <= nx < len(grid) and 0 <= ny < len(grid) and (grid[nx][ny] != "🔥" and grid[nx][ny] != "🟫"):
            return True
    return False