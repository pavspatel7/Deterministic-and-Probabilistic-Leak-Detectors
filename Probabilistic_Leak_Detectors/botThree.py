import random
from helperMethod import find_shortest_path, get_neighbors

class bot3():
    
    def __init__(self, getGrid, botpos, leakpos_1):
        
        self.grid = getGrid
        self.botpos = botpos
        self.leakpos_1 = leakpos_1
        # temp grid
        self.bot_3_grid = [row.copy() for row in self.grid]
        self.task_for_bot3()
        
        
    def task_for_bot3(self):
        for x in self.grid:
            print(''.join(x))
        print()
        
        
    
    
    