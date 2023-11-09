# import heapq

# def dijkstra(grid, source, target):
#     rows = len(grid)
#     cols = len(grid[0])
#     distances = [[float('inf')] * cols for _ in range(rows)]
#     distances[source[0]][source[1]] = 0
#     pq = [(0, source)]

#     directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

#     while pq:
#         dist, (x, y) = heapq.heappop(pq)

#         for dx, dy in directions:
#             nx, ny = x + dx, y + dy

#             if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == "O":
#                 new_dist = distances[x][y] + 1  # Assuming each step has a weight of 1

#                 if new_dist < distances[nx][ny]:
#                     distances[nx][ny] = new_dist
#                     heapq.heappush(pq, (new_dist, (nx, ny)))

#     # Check if the target is reachable
#     if distances[target[0]][target[1]] == float('inf'):
#         return "Target is not reachable"

#     return distances[target[0]][target[1]]

# grid = [
#     ["O", "B", "G"],
#     ["O", "B", "O"],
#     ["O", "O", "O"]
# ]

# source_cell = (0, 0)
# target_cell = (0, 2)

# distance = dijkstra(grid, source_cell, target_cell)
# if distance != "Target is not reachable":
#     print(f"Shortest distance to the target: {distance}")
# else:
#     print("Target is not reachable")

def get_dict(self, grid):
    my_dict = {}
    used_cells = set()
    grid_len = len(grid)

    for x in range(grid_len):
        for y in range(grid_len):
            cell_x_y = (x, y)
            if grid[x][y] != "⬛️":
                for i in range(x, grid_len):
                    for j in range(y, grid_len):
                        cell_i_j = (i, j)
                        if grid[i][j] != "⬛️" and cell_x_y != cell_i_j:
                            if ((cell_x_y, cell_i_j) not in used_cells and
                                    (cell_i_j, cell_x_y) not in used_cells):
                                my_dict[(cell_x_y, cell_i_j)] = 1
                                used_cells.add((cell_x_y, cell_i_j))
    return my_dict
