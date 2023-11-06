import random
from helperMethod import find_shortest_path, get_neighbors

class bot3():
    
    def _init_(self, getGrid, botpos, leakpos_1):
        
        self.grid = getGrid
        self.botpos = botpos
        self.leakpos_1 = leakpos_1
        # temp grid
        self.bot_3_grid = [row.copy() for row in self.grid]
        self.task_for_bot3(self.bot_3_grid)
        
        
    def task_for_bot3(self, grid):
        cell_probability_dict = {}
        open=0
        for x in grid:
            print(''.join(x))
        print()

        probability_grid = [row.copy() for row in self.grid]

        # In dictionary storing the cell:
        # 1) open and leak cell to by default probability is 
        # 1) block and bot cell to by default probability is 0
        for x in range(len(grid)):
            for y in range(len(grid)):
                if grid[x][y] == "⬜️" or grid[x][y] == "🟥":
                    open+=1
                    cell_probability_dict[(x,y)] = 1
                if grid[x][y] == "⬛️" or grid[x][y] == "😀":
                    cell_probability_dict[(x,y)] = 0


        
        for x in probability_grid:
            print(' '.join(x))
        print()